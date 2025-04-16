import pygame

from gameCode.Classes.gameObjectClass import GameObject
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.playerClass import Player
class Enemy(Physic):
    def __init__(self, x, y):
        self.image = pygame.image.load("./images/enemiesAnimation/ghost.png")
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height, 2, 5)
        self.health = 100
        self.direction = 1
        self.startPosition = x
        self.lastTriggerTime = 0
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.tag = "enemy"

    def tick(self, player):
        self.moveDirection(player)
        self.physicTick(player)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)


    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))
    def moveDirection(self, player):
        currentTime = pygame.time.get_ticks()
        cooldown = 500
        self.positionX -= self.acc * self.direction
        if(self.positionX == self.startPosition - 200):
            self.changeDirection()
        elif(self.positionX == self.startPosition + 200):
            self.changeDirection()
        elif(self.hitbox.colliderect(player.hitbox) and currentTime - self.lastTriggerTime >= cooldown):
            self.changeDirection()
            self.lastTriggerTime = currentTime
            player.health -= 10

    def changeDirection(self):
        self.direction *= -1
        self.positionX -= self.acc * self.direction
        if(self.direction > 0):
            self.image = pygame.image.load("./images/enemiesAnimation/ghost.png")
        else:
            self.image = pygame.image.load("./images/enemiesAnimation/ghost2.png")

