from math import floor

from gameCode.Classes.NPC.NPC import BaseNPC
from gameCode.Classes.UI.panels.questOfferPanel import QuestOfferPanel
from gameCode.fonts.fonts import addFont
from gameCode.images.animations import scaleAnimationFrames, load_animation_frames


class QuestNPC(BaseNPC):
    def __init__(self, x, y, quests):
        super().__init__(x, y, "./images/playerAnimation/nieUzywane/player0.png", 'Czajson')
        self.quests = quests
        self.questGiven = set()
        self.completed = set()
        self.panel = None
        self.dialogOpen = False
        self.image = scaleAnimationFrames(load_animation_frames(
            "./images/npc/animacjeNpc/sprite sheets/steampunk/masked_man.png", frame_width=32, frame_height=32, rows=1),
            (100, 100))
        self.standIndex = 0

    def tick(self, player):
        super().tick(player)

    def draw(self, window, cameraX=0, cameraY=0, player=None):
        self.standIndex = (self.standIndex + 0.1) % len(self.image)
        img = self.image[floor(self.standIndex)]
        window.blit(img, (self.positionX - cameraX, self.positionY - cameraY))
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
        if self.dialogOpen and self.panel:
            self.panel.draw(window)

    def interact(self, player):
        if not self.panel:
            self.panel = QuestOfferPanel(self, player)  # lub QuestOfferPanel
        else:
            self.panel.toggle()