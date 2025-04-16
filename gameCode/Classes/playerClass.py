import pygame
from math import floor

from gameCode.Classes.gameObjectClass import GameObject
from gameCode.Classes.physicClass import Physic
class Player(Physic):

    def __init__(self):
        self.standImage = pygame.image.load(f"./images/playerAnimation/player0.png")
        width = self.standImage.get_width()
        height = self.standImage.get_height()
        self.health = 100
        super().__init__(0, 600, width, height, 0.5, 5)
        self.jumpImg = pygame.image.load(f"./images/playerAnimation/player9.png")
        self.walkImg = [pygame.image.load(f"./images/playerAnimation/player{x}.png") for x in range(1, 7)]
        self.walkIndex = 4
        self.tag = "player"
        self.jumping = False


    def tick(self, keys, grounds):
        self.physicTick(grounds)
        if (keys[pygame.K_a] and self.horVelocity > self.maxVelocity * -1):
            self.horVelocity -= self.acc
        if (keys[pygame.K_d] and self.horVelocity < self.maxVelocity):
            self.horVelocity += self.acc
        if(keys[pygame.K_SPACE] and self.jumping == False):
            self.verVelocity -= 15
            self.jumping = True
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (self.horVelocity > 0):
                self.horVelocity -= self.acc
            elif(self.horVelocity < 0):
                self.horVelocity += self.acc
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def draw(self, window):
        if self.jumping:
            window.blit(self.jumpImg, (self.positionX, self.positionY))
        elif(self.horVelocity != 0):
            window.blit(self.walkImg[floor(self.walkIndex)], (self.positionX, self.positionY))
            self.walkIndex += 0.3
            print(self.walkIndex)
            if self.walkIndex > 5:
                self.walkIndex = 0
        else:
            window.blit(self.standImage, (self.positionX, self.positionY))

    def healthBar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (3, 3, self.width + 5, 15))
        pygame.draw.rect(window, (235, 64, 52), (5, 5, self.width * (self.health / 100), 10))
