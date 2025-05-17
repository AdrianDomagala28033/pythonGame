import pygame
import sys
from gameCode.Classes.UI.minimap import drawMiniMap
from gameCode.Classes.levels.levelManager import LevelManager
from gameCode.Classes.levels.levelLoading import load_from_file



def game(window):
    pygame.init()
    window_width = 1280
    window_height = 720
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("The last exit")
    clock = pygame.time.Clock()
    level_manager = LevelManager(window)

    try:
        tutorial_level = load_from_file("levels/levelsTXT/tutorial", window, onLevelChange=level_manager.nextLevel)
        level_manager.levels.append(tutorial_level)
        level_manager.currentLevelIndex = 0
        level_manager.map = ["".join(row) for row in open("levels/levelsTXT/tutorial")]
    except Exception as e:
        print("❌ Błąd ładowania poziomu:", e)
        pygame.quit()
        sys.exit()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_level = level_manager.getCurrentLevel()

        current_level.player.tick(keys, current_level.tiles, current_level.enemies, window)

        if current_level.door.tick(current_level.player, window):
            print("➡️ Przejście do kolejnego poziomu")
            new_level = level_manager.nextLevel()
            if new_level:
                current_level = new_level

        current_level.update_camera()
        current_level.update(current_level.tiles, window)

        window.fill((30, 30, 30))
        current_level.draw(window)

        if keys[pygame.K_m]:
            drawMiniMap(window, level_manager.map, current_level.player)

        pygame.display.flip()

    pygame.quit()
    sys.exit()