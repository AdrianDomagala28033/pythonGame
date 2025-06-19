import pygame
from gameCode.fonts.fonts import addFont


class CharacterMenu:
    def __init__(self, player, questManager):
        self.player = player
        self.questManager = questManager

        self.font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 28)

        self.width, self.height = 700, 500
        self.posX, self.posY = 300, 100

        self.bgColor = (20, 20, 20)
        self.fgColor = (255, 255, 255)
        self.hlColor = (0, 255, 0)
        self.borderColor = (255, 255, 255)

        self.tabs = ["stats", "inventory", "quests"]
        self.tabLabels = ["Statystyki", "Ekwipunek", "Questy"]
        self.tabIndex = 0  # aktywna zakładka (index)

        self.active = False

        self.surface = pygame.Surface((self.width, self.height))
        self.tabRects = []

        self.selectionIndex = 0

        self.itemRects = []
        self.hoveredItem = None
        self.draggedItem = None
        self.draggedFromIndex = None

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.tabIndex = 0
            self.selectionIndex = 0
        print(f"[CharacterMenu] Panel {'otwarty' if self.active else 'zamknięty'}")

    def handleEvent(self, event):
        if not self.active:
            return

        self.updateTabRects()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle()
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_TAB):
                self.tabIndex = (self.tabIndex + 1) % len(self.tabs)
                self.selectionIndex = 0
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.tabIndex = (self.tabIndex - 1) % len(self.tabs)
                self.selectionIndex = 0

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            localPos = (mx - self.posX, my - self.posY)
            for i, rect in enumerate(self.tabRects):
                if rect.collidepoint(localPos):
                    self.tabIndex = i
                    self.selectionIndex = 0
                    print(f"Zakładka zmieniona na: {self.tabLabels[self.tabIndex]}")  # debug
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.tabs[self.tabIndex] == "inventory":
                mx, my = event.pos
                localX, localY = mx - self.posX, my - self.posY
                slotSize = 50
                spacing = 10
                startX, startY = 20,60

                for i in range(4):
                    rect = pygame.Rect(startX + i * (slotSize + spacing), startY, slotSize, slotSize)
                    if rect.collidepoint((localX, localY)):
                        item = self.player.inventory.usableItems[i]
                        if item:
                            self.draggedItem = item
                            self.draggedFromIndex = i
                        return
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.draggedItem and self.draggedFromIndex is not None and self.tabs[self.tabIndex] == "inventory":
                mx, my = event.pos
                localX, localY = mx - self.posX, my - self.posY
                slotSize = 50
                spacing = 10
                startX, startY = 20,60
                for i in range(4):
                    rect = pygame.Rect(startX + i * (slotSize + spacing), startY, slotSize, slotSize)
                    if rect.collidepoint((localX, localY)):
                        inv = self.player.inventory.usableItems
                        inv[self.draggedFromIndex], inv[i] = inv[i], inv[self.draggedFromIndex]
                        break
                    self.draggedItem = None
                    self.draggedFromIndex = None

    def updateTabRects(self):
        self.tabRects = []
        startX = 20
        y = 10
        spacing = 20
        for i, label in enumerate(self.tabLabels):
            textSurface = self.font.render(label, True, self.fgColor)
            rect = pygame.Rect(startX, y, textSurface.get_width() + 20, 30)
            self.tabRects.append(rect)
            startX += rect.width + spacing

    def drawTabs(self, surface):
        for i, rect in enumerate(self.tabRects):
            bgColor = (60, 60, 60)
            pygame.draw.rect(surface, bgColor, rect)
            pygame.draw.rect(surface, self.borderColor, rect, 2)
            color = self.hlColor if i == self.tabIndex else self.fgColor
            label = self.tabLabels[i]
            textSurface = self.font.render(label, True, color)
            surface.blit(textSurface, (rect.x + 10, rect.y + 3))
        pygame.draw.line(surface, self.borderColor, (10, 45), (self.width - 10, 45))

    def draw(self, window):
        if not self.active:
            return

        self.surface.fill(self.bgColor)
        pygame.draw.rect(self.surface, self.borderColor, self.surface.get_rect(), 2)

        self.updateTabRects()
        self.drawTabs(self.surface)

        # Rysuj zawartość w zależności od aktywnej zakładki
        if self.tabs[self.tabIndex] == "stats":
            self.drawStats()
        elif self.tabs[self.tabIndex] == "inventory":
            self.drawInventory()
        else:
            self.drawQuests()

        window.blit(self.surface, (self.posX, self.posY))

        if self.draggedItem:
            icon = pygame.image.load(self.draggedItem.icon)
            mx, my = pygame.mouse.get_pos()
            self.surface.blit(icon, (mx - self.posX - 25, my - self.posY - 25))

    def drawStats(self):
        y = 60
        stats = [
            f"Poziom: {self.player.level}",
            f"XP: {self.player.xp} / {self.player.xpToNextLevel}",
            f"HP: {self.player.health} / {self.player.maxHealth}",
            f"Siła: {self.player.strength}",
            f"Obrona: {self.player.defense}",
            f"Szybkość: {self.player.speed}",
            f"Monety: {self.player.coins}",
            f"Punkty rozwoju: {self.player.upgradePoints}"
        ]
        for line in stats:
            textSurface = self.font.render(line, True, self.fgColor)
            self.surface.blit(textSurface, (20, y))
            y += 30

    def drawInventory(self):
        self.player.inventory.drawInventory(self.surface, x=20, y=60)
        if self.hoveredItem:
            desc = getattr(self.hoveredItem, "description", "Brak opisu.")
            textSurface = self.font.render(f"Opis: {desc}", True, (200,200,200))
            self.surface.blit(textSurface, (20,300))

        mx, my = pygame.mouse.get_pos()
        localX, localY = mx - self.posX, my - self.posY
        self.hoveredItem = None
        for i in range(4):
            rect = pygame.Rect(20 + i * (50 + 10), 60, 50, 50)
            if rect.collidepoint((localX, localY)):
                item = self.player.inventory.usableItems[i]
                if item:
                    self.hoveredItem = item
                    pygame.draw.rect(self.surface, (0, 255, 0), rect, 2)

    def drawQuests(self):
        y = 60
        quests = self.questManager.getActiveQuests()
        if not quests:
            self.surface.blit(self.font.render("Brak aktywnych zadań", True, (150, 150, 150)), (20, y))
            return
        for quest in quests:
            status = "✓" if quest.completed else "-"
            progressText = ""
            if hasattr(quest, "progress") and hasattr(quest, "requiredAmount"):
                progressText = f" ({quest.progress}/{quest.requiredAmount}"
            text = f"[{status}] {quest.name}{progressText}"
            if quest.completed:
                color = (0, 255, 0)
            elif quest.progress == 0:
                color = (180, 180, 180)
            else:
                color = self.fgColor
            textSurface = self.font.render(text, True, color)
            self.surface.blit(textSurface, (20, y))
            y += 30
