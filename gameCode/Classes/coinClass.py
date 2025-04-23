import pygame
from random import randint
from gameCode.Classes.gameObjectClass import GameObject

class Coin(GameObject):
    def __init__(self, x, y):
        self.value = 1
        self.positionX = x
        self.positionY = y
        self.image = pygame.image.load("./images/coin.PNG")
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.tag = "coin"

    def tick(self, player):
        if(self.hitbox.colliderect(player.hitbox)):
            player.coins += self.value
            return True
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))


