import pygame
class Player:

    def __init__(self):
        self.positionX = 0
        self.positionY = 580
        self.image = pygame.image.load("./images/player.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 2
        self.health = 100
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self, keys):
        if keys[pygame.K_w]:
            self.positionY -= self.speed
        if keys[pygame.K_s]:
            self.positionY += self.speed
        if keys[pygame.K_a]:
            self.positionX -= self.speed
        if keys[pygame.K_d]:
            self.positionX += self.speed
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))
