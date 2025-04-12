import pygame
class Enemy:
    def __init__(self):
        self.positionX = 600
        self.positionY = 400
        self.image = pygame.image.load("./images/ghost.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 2
        self.health = 100
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.direction = 1

    def tick(self):
        self.moveDirection()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)


    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))
    def moveDirection(self):
        self.positionX -= self.speed * self.direction
        if (self.positionX == 20):
            self.direction *= -1
            self.image = pygame.image.load("./images/ghost2.png")
        elif (self.positionX == 1200):
            self.direction *= -1
            self.image = pygame.image.load("./images/ghost.png")