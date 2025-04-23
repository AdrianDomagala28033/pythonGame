import pygame

class GameObject:
    def __init__(self, x, y, width, height, tag="neutral"):
        self.positionX = x
        self.positionY = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(x, y, width, height)
        self.tag = tag  # np. "platforma", "enemy", "drzwi"

    def draw(self, surface, color=(200, 200, 200)):
        pygame.draw.rect(surface, color, self.hitbox)

    def draw_relative(self, window, cameraX):
        window.blit(self.image, (self.positionX - cameraX, self.positionY))

