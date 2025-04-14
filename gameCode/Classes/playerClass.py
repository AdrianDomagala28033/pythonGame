import pygame
from physicClass import Physic
class Player(Physic):

    def __init__(self):
        self.positionX = 0
        self.positionY = 580
        self.image = pygame.image.load("./images/player.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.horVelocity = 0
        self.acc = 0.5
        self.maxVelocity = 5
        self.health = 100
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self, keys):
        if (keys[pygame.K_a] and self.horVelocity > self.maxVelocity * -1):
            self.horVelocity -= self.acc
        if (keys[pygame.K_d] and self.horVelocity < self.maxVelocity):
            self.horVelocity += self.acc
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (self.horVelocity > 0):
                self.horVelocity -= self.acc
            elif(self.horVelocity < 0):
                self.horVelocity += self.acc
        print(self.horVelocity)
        self.positionX += self.horVelocity
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))
