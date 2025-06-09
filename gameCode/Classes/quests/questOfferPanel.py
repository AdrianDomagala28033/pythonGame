import pygame
from gameCode.fonts.fonts import addFont

class QuestOfferPanel:
    def __init__(self, npc, player):
        self.npc = npc
        self.player = player
        self.active = False
        self.font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 24)
        self.buttonHeight = 40
        self.margin = 10
        self.buttons = []
        self.hoveredQuest = None

        self.notificationTimer = 0
        self.lastAddedQuest = None

        self.generateButtons()

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
        if not self.active:
            self.hoveredQuest = None

    def draw(self, surface):
        if not self.active:
            return

        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        title = self.font.render("Wybierz quest:", True, (255, 255, 255))
        surface.blit(title, (320, 150))

        mousePos = pygame.mouse.get_pos()
        self.hoveredQuest = None

        for quest, rect in self.buttons:
            if rect.collidepoint(mousePos):
                self.hoveredQuest = quest

            if quest in self.player.questManager.quests:
                if quest.completed and not quest.delivered:
                    color = (0, 150, 0)  # Zielony – można odebrać nagrodę
                elif quest.delivered:
                    color = (100, 100, 100)  # Szary – już odebrany
                else:
                    color = (70, 70, 200)  # Niebieski – aktywny
            else:
                color = (40, 40, 40)
            pygame.draw.rect(surface, color, rect)
            text = self.font.render(quest.name, True, (255, 255, 255))
            surface.blit(text, (rect.x + 10, rect.y + 5))

        # Podgląd hoverowanego questa
        if self.hoveredQuest:
            boxX = 750
            boxY = 200
            pygame.draw.rect(surface, (40, 40, 40), (boxX, boxY, 400, 120))
            lines = [
                f"Nazwa: {self.hoveredQuest.name}",
                f"Opis: {self.hoveredQuest.description}",
                f"Cel: {self.hoveredQuest.requiredAmount} {self.hoveredQuest.target}",
                f"Nagroda: 25 złota, 50 XP"
            ]
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (255, 255, 255))
                surface.blit(text, (boxX + 10, boxY + 10 + i * 25))

        # Powiadomienie o dodaniu questa
        if self.lastAddedQuest and pygame.time.get_ticks() - self.notificationTimer < 2000:
            text = self.font.render(f"📜 Dodano: {self.lastAddedQuest.name}", True, (255, 255,255))
            surface.blit(text, (320, 150 + len(self.buttons) * (self.buttonHeight + self.margin) + 20))

    def handleEvent(self, event):
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for quest, rect in self.buttons:
                if rect.collidepoint(mouse_pos):
                    if quest.completed and not quest.delivered:
                        # Nagroda za wykonany quest
                        self.player.coins += 25
                        self.player.gainXP(50)
                        quest.delivered = True
                        self.lastAddedQuest = quest
                        self.notificationTimer = pygame.time.get_ticks()
                        print(f"🏁 Quest oddany: {quest.name}")
                        if quest in self.player.questManager.quests:
                            self.player.questManager.quests.remove(quest)
                            self.generateButtons()
                    elif quest not in self.player.questManager.quests:
                        self.player.questManager.addQuest(quest)
                        self.npc.questGiven.add(quest)
                        self.lastAddedQuest = quest
                        self.notificationTimer = pygame.time.get_ticks()
                        print(f"✅ Dodano questa: {quest.name}")
                    break  # dodaj tylko jeden quest

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle()
