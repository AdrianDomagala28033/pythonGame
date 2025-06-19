import pygame


class BaseNPC:
    def __init__(self, x, y, imagePath, name):
        self.positionX = x
        self.positionY = y
        self.image = pygame.image.load(imagePath)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.dialogVisible = False
        self.type = ''
        self.name = name

    def tick(self, player):
        self.dialogVisible = self.hitbox.colliderect(player.hitbox)
    def draw(self, window, cameraX=0, cameraY=0):
        window.blit(self.image, (self.positionX - cameraX, self.positionY - cameraY))
    def isNearPlayer(self, player):
        return (abs(player.positionX - self.positionX) < 120 and abs(player.positionY - self.positionY) < 50)