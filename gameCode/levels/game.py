import pygame
import sys

from gameCode.Classes.UI.panels.CharacterMenu import CharacterMenu
from gameCode.Classes.UI.chestInventory import InventoryUiExchange
from gameCode.Classes.UI.dialogBox import DialogBox
from gameCode.Classes.UI.minimap import drawMiniMap
from gameCode.Classes.levels.levelManagment.levelManager import LevelManager
from gameCode.Classes.levels.levelManagment.levelLoading import load_from_file
from gameCode.fonts.fonts import addFont


def game(window):
    pygame.init()
    window_width = 1280
    window_height = 720
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("The last exit")
    clock = pygame.time.Clock()
    level_manager = LevelManager(window)
    inventoryUI = None
    characterPanel = None
    gamePaused = False
    questPanel = None
    dialogBox = None
    font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 28)

    try:
        hub_level = load_from_file("levels/levelsTXT/tutorial", window, onLevelChange=level_manager.nextLevel)
        level_manager.levels.append(hub_level)
        level_manager.currentLevelIndex = 0
        level_manager.map = ["".join(row) for row in open("levels/levelsTXT/tutorial")]

        # ✅ Stworzenie panelu postaci RAZ, po wczytaniu poziomu
        current_level = level_manager.getCurrentLevel()
        characterPanel = CharacterMenu(hub_level.player, current_level.player.questManager)

    except Exception as e:
        print("❌ Błąd ładowania poziomu:", e)
        pygame.quit()
        sys.exit()

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        # ========== 1. OBSŁUGA ZDARZEŃ ==========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 1A. DialogBox ma najwyższy priorytet
            if dialogBox and dialogBox.active:
                dialogBox.handleEvent(event)
                continue

            # 1B. NPC Panel — dowolny aktywny panel NPC (quest, upgrade)
            npcPanelHandled = False
            for npc in current_level.NPCs:
                if getattr(npc, "dialogOpen", False) and hasattr(npc, "panel"):
                    npc.panel.handleEvent(event)
                    npcPanelHandled = True
                    break
            if npcPanelHandled:
                continue  # ignoruj inne inputy

            # 1C. Inventory / skrzynia
            if inventoryUI and inventoryUI.active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    inventoryUI.toggle()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    inventoryUI.handleClick(pygame.mouse.get_pos())
                continue

            # 1D. Panel postaci
            if characterPanel and characterPanel.active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    characterPanel.toggle()
                else:
                    characterPanel.handleEvent(event)
                continue

            # 1E. Obsługa H — powrót do huba
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                def goToHub():
                    newHubLevel = load_from_file("levels/levelsTXT/tutorial", window,
                                                 onLevelChange=level_manager.nextLevel)
                    level_manager.levels = [newHubLevel]
                    level_manager.currentLevelIndex = 0
                    level_manager.map = ["".join(row) for row in open("levels/levelsTXT/tutorial")]
                    # Aktualizacja referencji do gracza
                    current_level = level_manager.getCurrentLevel()
                    characterPanel.player = current_level.player
                    characterPanel.questManager = current_level.player.questManager

                dialogBox = DialogBox("Czy chcesz wrócić do lobby?", [("Tak", goToHub), ("Nie", None)], font)
                continue

            # 1F. Otwieranie paneli NPC przez E
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for npc in current_level.NPCs:
                    if npc.isNearPlayer(current_level.player):
                        npc.interact(current_level.player)
                        break  # Tylko jeden NPC

            # Obsługa paneli NPC
            for npc in current_level.NPCs:
                if hasattr(npc, "panel") and npc.dialogOpen and npc.panel.active:
                    npc.panel.handleEvent(event)
                    break

            # 1G. TAB — otwieranie panelu postaci
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                if characterPanel:
                    characterPanel.toggle()

        # ========== 2. AUTOMATYCZNA PAUZA ==========
        gamePaused = (
                (inventoryUI and inventoryUI.active) or
                (characterPanel and characterPanel.active) or
                (dialogBox and dialogBox.active) or
                any(getattr(npc, "dialogOpen", False) for npc in current_level.NPCs)
        )

        # ========== 3. TICK / LOGIKA GRY ==========
        keys = pygame.key.get_pressed()
        current_level = level_manager.getCurrentLevel()
        if not gamePaused:
            current_level.player.tick(keys, current_level.tiles, current_level.enemies, window)

            for chest in current_level.chests:
                chest.tick(current_level.player)
                if chest.opened and not chest.uiOpened:
                    inventoryUI = InventoryUiExchange(current_level.player.inventory, chest.inventory)
                    inventoryUI.toggle()
                    chest.uiOpened = True
                    print("✅ Otwieram interfejs skrzyni")

        if current_level.door.tick(current_level.player, window):
            print("➡️ Przejście do kolejnego poziomu")
            new_level = level_manager.nextLevel()
            characterPanel.player = new_level.player
            characterPanel.questManager = new_level.player.questManager

        # ========== 4. AKTUALIZACJE ==========
        current_level.update_camera()
        current_level.update(current_level.tiles, window)

        # ========== 5. RYSOWANIE ==========
        window.fill((30, 30, 30))
        current_level.draw(window)

        if keys[pygame.K_m]:
            drawMiniMap(window, level_manager.map, current_level.player)

        if inventoryUI and inventoryUI.active:
            inventoryUI.draw(window)

        if characterPanel and characterPanel.active:
            characterPanel.draw(window)

        for npc in current_level.NPCs:
            if getattr(npc, "dialogOpen", False) and hasattr(npc, "panel"):
                npc.panel.draw(window)

        if dialogBox and dialogBox.active:
            dialogBox.draw(window)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

def drawNpcPanels(npcs, window):
    for npc in npcs:
        if getattr(npc, "dialogOpen", False) and hasattr(npc, "panel"):
            npc.panel.draw(window)