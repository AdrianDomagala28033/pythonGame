import pygame
from gameCode.Classes.gameObjectClass import GameObject

class Ground(GameObject):
    def __init__(self, x, y, image):
        self.image = image
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))