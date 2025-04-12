import pygame

class Ground:
    def __init__(self):
        self.positionX = 0
        self.positionY = 670
        self.image = pygame.image.load("./images/ground.PNG")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, window):
        for x in range(0, 1280, 50):
            window.blit(self.image, (x, 680))