from math import floor

import pygame

from gameCode.Classes.NPC.NPC import BaseNPC
from gameCode.Classes.UI.panels.upgradePanel import UpgradePanel
from gameCode.fonts.fonts import addFont
from gameCode.images.animations import load_animation_frames, scaleAnimationFrames


class UpgradeNPC(BaseNPC):
    def __init__(self, x, y, imagePath, name):
        super().__init__(x,y,imagePath,name)
        self.dialogOpen = False
        self.currentTreeKey = "player"
        self.selectionIndex = 0
        self.panel = None
        self.image = scaleAnimationFrames(load_animation_frames(
            "./images/npc/animacjeNpc/sprite sheets/medieval/blacksmith.png", frame_width=34, frame_height=34, rows=1), (100, 100))
        self.standIndex = 0
    def interact(self, player):
        if not self.panel:
            self.panel = UpgradePanel(self, player)  # lub QuestOfferPanel
        else:
            self.panel.toggle()

    def handleInput(self, player, keys):
        if self.panel and self.dialogOpen:
            pass

    def draw(self, window, cameraX=0, cameraY=0, player=None):
        self.standIndex = (self.standIndex + 0.1) % len(self.image)
        img = self.image[floor(self.standIndex)]
        window.blit(img, (self.positionX - cameraX, self.positionY - cameraY))
        if self.panel and self.dialogOpen:
            self.panel.draw(window)