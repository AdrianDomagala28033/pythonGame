import pygame
import random

from gameCode.Classes.UI.InventoryItems.potions import health_potion
from gameCode.Classes.levels.levelElements.objects import Object


class Chest(Object):
    def __init__(self, x, y):
        self.positionX = x
        self.positionY = y
        self.fullChestImages = [pygame.image.load(f"./images/chestAnimation/chest{x+1}.png") for x in range(3)]
        self.emptyChestImages = [pygame.image.load(f"./images/chestAnimation/emptyChest/chest{x+1}.png") for x in range(3)]
        self.image = pygame.image.load(f"./images/chestAnimation/chest1.png")
        self.chestIndex = 1
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.visionRange = 50
        super().__init__(x, y,"Chest", "Skrzynia z przedmiotami", "./images/chest.png", "chest")
        self.opened = False
        self.usable = False
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def tick(self, player):
        self.detectPlayer(player)
        self.useObject(player)
    def draw(self, window, cameraX, cameraY):
            window.blit(self.image, (self.positionX - cameraX, self.positionY - cameraY))
    def detectPlayer(self, player):
        rightVision = pygame.Rect(self.positionX, self.positionY, self.visionRange, self.height)
        leftVision = pygame.Rect(self.positionX - self.visionRange, self.positionY, self.visionRange, self.height)
        if rightVision.colliderect(player.hitbox) or leftVision.colliderect(player.hitbox):
            self.chestIndex += 0.3
            if self.chestIndex >= len(self.isEmpty()):
                self.chestIndex = len(self.isEmpty()) - 1
        else:
            self.chestIndex -= 0.3
            if self.chestIndex < 0:
                self.chestIndex = 0
        image = self.isEmpty()
        self.image = image[int(self.chestIndex)]
        self.usable = True
    def isEmpty(self):
        if self.opened:
            return self.emptyChestImages
        else:
            return self.fullChestImages
    def useObject(self, player):
        if player.hitbox.colliderect(self.hitbox) and player.wantInteract and not self.opened:
            player.inventory.addItem(health_potion)
            player.coins += random.randint(0, 5)
            self.opened = True