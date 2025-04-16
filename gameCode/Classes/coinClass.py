import pygame
from random import randint
from gameCode.Classes.gameObjectClass import GameObject

class Coin(GameObject):
    def __init__(self):
        self.value = 1
        self.positionX = randint(0, 1280)
        self.positionY = randint(0, 680)
        self.image = pygame.image.load("./images/coin.PNG")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self):
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))


