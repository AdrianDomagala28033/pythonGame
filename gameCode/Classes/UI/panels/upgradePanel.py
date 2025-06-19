from types import SimpleNamespace

import pygame

from gameCode.Classes.UI.panels.basePanel import BaseNpcPanel
from gameCode.Classes.UI.panels.utils import getHoverIndex, drawPanelBackground, drawHighlightedText
from gameCode.fonts.fonts import addFont
from gameCode.images.animations import scaleAnimationFramesToDoubleSize, load_animation_frames


class UpgradePanel(BaseNpcPanel):
    def __init__(self, npc, player):
        super().__init__(npc, player)
        self.font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 24)
        self.selectionIndex = 0
        self.active = False
        self.npc.dialogOpen = True
        self.buttons = []
        self.tabRects = []
        self.tabs = ["player", "bow", "sword"]
        self.tabLabels = ["Gracz", "Łuk", "Miecz"]
        self.tabIndex = 0
        self.treeKey = self.tabs[self.tabIndex]
        self.toggle()
        self.idleAnim = scaleAnimationFramesToDoubleSize(
            load_animation_frames("./images/playerAnimation/idleCharacter.png", 19, 30, 1)
        )
        self.animFrame = 0

    def toggle(self):
        self.active = not self.active
        self.npc.dialogOpen = self.active
        print(f"🔁 toggle panel — active: {self.active}")
        self.updateButtonRects()


    def handleEvent(self, event):
        if not self.active:
            return
        super().handleEvent(event)  # ESC zamyka panel
        self.updateTabRects()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.tabIndex = (self.tabIndex - 1) % len(self.tabs)
                self.treeKey = self.tabs[self.tabIndex]
                self.selectionIndex = 0
                self.updateButtonRects()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.tabIndex = (self.tabIndex + 1) % len(self.tabs)
                self.treeKey = self.tabs[self.tabIndex]
                self.selectionIndex = 0
                self.updateButtonRects()
            elif event.key in (pygame.K_w, pygame.K_UP):
                self.selectionIndex = (self.selectionIndex - 1) % len(self.buttons)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.selectionIndex = (self.selectionIndex + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.tryUnlockSelectedNode()

        if event.type == pygame.MOUSEMOTION:
            hover = getHoverIndex(self.buttons, pygame.mouse.get_pos())
            if hover is not None:
                self.selectionIndex = hover
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.tabRects):
                if rect.collidepoint(mouse_pos):
                    self.tabIndex = i
                    self.treeKey = self.tabs[self.tabIndex]
                    self.selectionIndex = 0
                    self.updateButtonRects()
                    return  # 👈 zakończ — NIE klikaj umiejętności!

            # 🔹 Klik na przycisk umiejętności
            if self.selectionIndex < len(self.buttons):
                self.tryUnlockSelectedNode()

    def currentNodeIds(self):
        return list(self.player.skillTrees[self.tabs[self.tabIndex]].nodes.keys())

    def draw(self, surface):
        img = self.idleAnim[int(self.animFrame) % len(self.idleAnim)]
        self.animFrame += 0.1
        surface.blit(img, (900, 40))
        if not self.active:
            return
        self.updateTabRects()
        for i, rect in enumerate(self.tabRects):
            selected = i == self.tabIndex
            drawHighlightedText(surface, rect, self.tabLabels[i], self.font, selected)

        panel = drawPanelBackground(surface, 700, 500)
        surface.blit(panel, (100, 100))


        tree = self.player.skillTrees[self.treeKey]
        nodeIds = self.currentNodeIds()
        self.updateButtonRects()

        # Zakładki
        self.drawTabs(surface)

        # Lista ulepszeń
        for i, (nodeId, rect) in enumerate(self.buttons):
            node = tree.nodes[nodeId]
            unlocked = nodeId in tree.unlockedNodes
            text = f"[{'X' if unlocked else ' '}] {node.name} ({node.cost} pkt)"
            color = (0, 255, 0) if unlocked else (255, 255, 255)
            selected = i == self.selectionIndex
            drawHighlightedText(surface, rect, text, self.font, selected, color)

        # Opis wybranego
        if self.selectionIndex < len(nodeIds):
            node = tree.nodes[nodeIds[self.selectionIndex]]
            desc = self.font.render(f"🛈 {node.description}", True, (200, 200, 200))
            surface.blit(desc, (120, 420))

        # Punkty rozwoju
        points = self.font.render(f"Punkty rozwoju: {self.player.upgradePoints}", True, (255, 255, 100))
        surface.blit(points, (120, 460))

        self.drawPlayerStats(surface)

    def drawPlayerStats(self, surface):
        if self.treeKey == "player":
            self.drawPlayerStatsPanel(surface)
        elif self.treeKey == "bow":
            self.drawBowStatsPanel(surface)
        elif self.treeKey == "sword":
            self.drawSwordStatsPanel(surface)

    def tryUnlockSelectedNode(self):
        nodeIds = self.currentNodeIds()
        if self.selectionIndex >= len(nodeIds):
            return

        nodeId = nodeIds[self.selectionIndex]
        tree = self.player.skillTrees[self.treeKey]

        if nodeId in tree.unlockedNodes:
            return  # już odblokowane

        # ➡ wybieramy właściwy obiekt do modyfikacji
        target = self.player  # domyślnie gracz
        if self.treeKey == "bow":
            target = self.player.inventory.getWeaponByTag("bow")
        elif self.treeKey == "sword":
            target = self.player.inventory.getWeaponByTag("sword")

        if target == self.player:  # bezpieczeństwo
            tree.unlock(nodeId, target)
        else:
            tree.unlockToWeapon(nodeId, self.player, target)
    def updateButtonRects(self):
        self.buttons = []
        y = 160
        for nodeId in self.currentNodeIds():
            rect = pygame.Rect(110, y, 580, 30)
            self.buttons.append((nodeId, rect))
            y += 30
    def drawTabs(self, surface):
        self.tabRects = []
        startX = 120
        y = 120
        for i, label in enumerate(self.tabLabels):
            rect = pygame.Rect(startX + i * 130, y, 120, 30)
            selected = i == self.tabIndex
            drawHighlightedText(surface, rect, label, self.font, selected)
    def updateTabRects(self):
        self.tabRects = []
        startX = 120
        y = 120
        for i, label in enumerate(self.tabLabels):
            rect = pygame.Rect(startX + i * 130, y, 120,30)
            self.tabRects.append(rect)
    def simulatePlayerEffect(self, effectFunc):
        class FakePlayer:
            def __init__(self, real):
                self.__dict__ = real.__dict__.copy()

        fake = FakePlayer(self.player)
        effectFunc(fake)

        result = {}
        for attr in ["strength", "defense", "speed", "maxHealth"]:
            before = getattr(self.player, attr)
            after = getattr(fake, attr)
            if after != before:
                statName = {
                    "strength": "Siła",
                    "defense": "Obrona",
                    "speed": "Szybkość",
                    "maxHealth": "HP"
                }.get(attr, attr)
                result[statName] = after
        return result

    def _simulateWeaponEffect(self, weapon, effectFunc, attrs, labels):
        # 1. Tworzymy "wydmuszkę" broni tylko z potrzebnymi polami
        fake = SimpleNamespace(**{a: getattr(weapon, a) for a in attrs})

        # 2. Symulujemy efekt na sztucznej broni
        effectFunc(fake)

        # 3. Zwracamy różnice
        result = {}
        for attr in attrs:
            before = getattr(weapon, attr)
            after = getattr(fake, attr)
            if after != before:
                result[labels.get(attr, attr)] = after
        return result

    def simulateBowEffect(self, effectFunc):
        bow = self.player.inventory.getWeaponByTag("bow")
        if not bow:
            return {}
        return self._simulateWeaponEffect(
            bow, effectFunc,
            ["damage", "cooldown"],
            {"damage": "Obrażenia", "cooldown": "Cooldown"}
        )
    def simulateSwordEffect(self, effectFunc):
        sword = self.player.inventory.getWeaponByTag("sword")
        if not sword:
            return {}
        result = self._simulateWeaponEffect(
            sword, effectFunc,
            ["damage", "range", "cooldown"],
            {"damage": "Obrażenia", "range": "Zasięg", "cooldown": "Cooldown"}
        )
        return result

    def drawPlayerStatsPanel(self, surface):
        self.drawStatsBox(surface, {
            "Siła": self.player.strength,
            "Obrona": self.player.defense,
            "Szybkość": self.player.speed,
            "HP": self.player.maxHealth
        })

    def drawBowStatsPanel(self, surface):
        bow = self.player.inventory.getWeaponByTag("bow")
        if not bow: return
        self.drawStatsBox(surface, {
            "Obrażenia": bow.damage,
            "Cooldown": bow.cooldown
        })

    def drawSwordStatsPanel(self, surface):
        sword = self.player.inventory.getWeaponByTag("sword")
        if not sword: return
        self.drawStatsBox(surface, {
            "Obrażenia": sword.damage,
            "Zasięg": sword.range,
            "Cooldown": sword.cooldown
        })

    def drawStatsBox(self, surface, param):
        panel_x = 840
        panel_y = 100
        panel_width = 360
        panel_height = 400
        # Tło
        pygame.draw.rect(surface, (20, 20, 20), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(surface, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)

        # Nagłówek
        header = self.font.render("Statystyki gracza", True, (255, 255, 255))
        surface.blit(header, (panel_x + 20, panel_y + 15))

        y = panel_y + 50
        spacing = 32
        # Podgląd po ulepszeniu
        preview = {}
        tree = self.player.skillTrees[self.treeKey]
        nodeIds = self.currentNodeIds()

        if self.selectionIndex < len(nodeIds):
            nodeId = nodeIds[self.selectionIndex]
            if nodeId not in tree.unlockedNodes:
                effect = tree.nodes[nodeId].effect
                if effect and tree == self.player.skillTrees["player"]:
                    preview = self.simulatePlayerEffect(effect)
                elif effect and tree == self.player.skillTrees["bow"]:
                    preview = self.simulateBowEffect(effect)
                elif effect and tree == self.player.skillTrees["sword"]:
                    preview = self.simulateSwordEffect(effect)

        for stat, value in param.items():
            new_val = preview.get(stat, value)
            color = (0, 255, 0) if new_val > value else (255, 255, 255)
            suffix = f" → {new_val}" if new_val != value else ""
            text = self.font.render(f"{stat}: {value}{suffix}", True, color)
            surface.blit(text, (panel_x + 20, y))
            y += spacing
