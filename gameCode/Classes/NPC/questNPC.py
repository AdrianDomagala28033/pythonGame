import pygame.key

from gameCode.Classes.NPC.NPC import BaseNPC
from gameCode.fonts.fonts import addFont


class QuestNPC(BaseNPC):
    def __init__(self, x, y, quests):
        super().__init__(x, y, "./images/playerAnimation/nieUzywane/player0.png", 'Czajson')
        self.quests = quests
        self.questGiven = set()
        self.completed = set()


    def tick(self, player):
        super().tick(player)

    def draw(self, window, cameraX=0, cameraY=0):
        super().draw(window, cameraX, cameraY)
        if self.dialogVisible:
            font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 24)
            availableQuests = [q for q in self.quests if q not in self.questGiven]
            completedQuests = [q for q in self.questGiven if q.completed and q not in self.completed]

            if availableQuests:
                text = font.render("Naciśnij E, aby porozmawiać", True, (255, 255, 0))
                window.blit(text, (self.positionX - cameraX - 20, self.positionY - 40 - cameraY))
            elif completedQuests:
                text = font.render("Naciśnij E, aby oddać zadanie", True, (0, 255, 0))
                window.blit(text, (self.positionX - cameraX - 20, self.positionY - 40 - cameraY))

    def isNearPlayer(self, player):
        return abs(player.positionX - self.positionX) < 50 and abs(player.positionY - self.positionY) < 50