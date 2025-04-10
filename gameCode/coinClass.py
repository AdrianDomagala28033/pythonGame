import pygame
from random import randint
from playerClass import Player
class Coin:
    def __init__(self):
        self.value = 1
        self.positionX = randint(0, 1280)
        self.positionY = randint(0, 720)
        self.image = pygame.image.load("images/coin.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self):
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))

    def createCoin(self, clock, player):
        score = 0
        coins = []
        if clock >= 2:
            clock = 0
            coins.append(Coin())
        for coin in coins:
            coin.tick()
