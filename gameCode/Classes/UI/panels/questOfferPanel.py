import pygame

from gameCode.Classes.UI.panels.basePanel import BaseNpcPanel
from gameCode.Classes.UI.panels.utils import getHoverIndex, drawHighlightedText, drawPanelBackground
from gameCode.fonts.fonts import addFont

class QuestOfferPanel(BaseNpcPanel):
    def __init__(self, npc, player):
        super().__init__(npc, player)
        self.font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 24)
        self.buttonHeight = 40
        self.margin = 10
        self.buttons = []
        self.hoveredQuest = None
        self.notificationTimer = 0
        self.lastAddedQuest = None
        self.generateButtons()
        self.active = True
        self.npc.dialogOpen = True
        self.selectionIndex = 0

    def generateButtons(self):
        self.buttons = []
        x = 300
        y = 200
        for quest in self.npc.quests:
            if quest.delivered:
                continue  # Pomijaj odebrane
            rect = pygame.Rect(x, y, 400, self.buttonHeight)
            self.buttons.append((quest, rect))
            y += self.buttonHeight + self.margin

    def toggle(self):
        self.active = not self.active
        self.npc.dialogOpen = self.active  # ← to sprawia że gra wie, czy ma pauzować
        if not self.active:
            self.hoveredQuest = None

    def draw(self, surface):
        if not self.active:
            return
        overlay = drawPanelBackground(surface, 1280, 720, alpha=180)
        surface.blit(overlay, (0,0))

        title = self.font.render(f"Zadania od {self.npc.name}", True, (255,255,255))
        surface.blit(title, (320, 150))

        mousePos = pygame.mouse.get_pos()

        for i, (quest, rect) in enumerate(self.buttons):
            selected = i == self.selectionIndex

            if quest in self.player.questManager.quests:
                if quest.completed and not quest.delivered:
                    color = (0, 200, 0)
                elif quest.delivered:
                    color = (100,100,100)
                else:
                    color = (70,70,70)
            else:
                color = (200,200,200)
            drawHighlightedText(surface, rect, quest.name, self.font, selected, color)

        if self.buttons and self.selectionIndex < len(self.buttons):
            quest, _ = self.buttons[self.selectionIndex]
            boxX, boxY = 750, 200
            pygame.draw.rect(surface, (40,40,40), (boxX, boxY, 400, 150))
            lines = [
                f"Nazwa: {quest.name}",
                f"Opis: {quest.description}",
                f"Cel: {quest.requiredAmount} {quest.target}",
                f"Nagroda: 25 złota, 50 XP"
            ]
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (255,255,255))
                surface.blit(text, (boxX + 10, boxY + 10 + i * 25))
        if self.lastAddedQuest and pygame.time.get_ticks() - self.notificationTimer < 2000:
            text = self.font.render(f"Dodano: {self.lastAddedQuest.name}", True, (255,255,255))
            surface.blit(text, (320, 600))



    def handleEvent(self, event):
        if not self.active:
            return
        super().handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.selectionIndex = (self.selectionIndex - 1) % len(self.buttons)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.selectionIndex = (self.selectionIndex + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN and self.selectionIndex < len(self.buttons):
                quest, _ = self.buttons[self.selectionIndex]
                self.selectQuest(quest)

        if event.type == pygame.MOUSEMOTION:
            hover = getHoverIndex(self.buttons, pygame.mouse.get_pos())
            if hover is not None:
                self.selectionIndex = hover

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.selectionIndex < len(self.buttons):
                quest, _ = self.buttons[self.selectionIndex]
                self.selectQuest(quest)

    def selectQuest(self, quest):
        if quest.completed and not quest.delivered:
            self.player.coins += 25
            self.player.gainXP(50)
            quest.delivered = True
            self.lastAddedQuest = quest
            self.notificationTimer = pygame.time.get_ticks()
            print(f"Quest oddany {quest.name}")
            if quest in self.player.questManager.quests:
                self.player.questManager.quests.remove(quest)
                self.generateButtons()
        elif quest not in self.player.questManager.quests:
            self.player.questManager.addQuest(quest)
            self.npc.questGiven.add(quest)
            self.lastAddedQuest = quest
            self.notificationTimer = pygame.time.get_ticks()
            print(f"Dodano questa {quest.name}")