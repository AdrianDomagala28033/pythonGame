import pygame

class Background:
    def __init__(self,x, y, image):
        self.positionX = x
        self.positionY = y
        self.image = image

    def tick(self, window):
        pass
    def draw(self, window):
        window.blit(self.image, (self.positionX, self.positionY))
