import pygame

from gameCode.Classes.coinClass import Coin
from gameCode.Classes.levels.levelElements.key import Key


class DroppedItem:
    def __init__(self, x, y, item, icon):
        self.positionX = x
        self.positionY = y
        self.item = item  # string lub Item()
        self.icon = pygame.image.load(icon)
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, window, cameraX, cameraY):
        window.blit(self.icon, (self.positionX - cameraX, self.positionY - cameraY))

    def checkPickup(self, player):
        if player.hitbox.colliderect(self.rect):
            if isinstance(self.item, str):
                if self.item == "coin":
                    player.coins += 1
                elif self.item == "key":
                    player.hasKey = True
            else:
                player.inventory.addItem(self.item)
            return True
        return False
