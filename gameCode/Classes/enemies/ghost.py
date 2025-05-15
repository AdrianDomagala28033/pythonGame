import pygame
from pygame.examples.cursors import image

from gameCode.Classes.enemies.enemyClass import Enemy


class GhostEnemy(Enemy):
    def __init__(self,x, y, damage, health, image=pygame.image.load("./images/enemiesAnimation/ghost.png")):
        super().__init__(x, y, image)
        self.image = image
        self.damage = damage
        self.health = health
        self.tag = "ghost"

    def tick(self, player, obstacles, window):
        self.physicTick(player, obstacles)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.patrol()
    def patrol(self):
        self.positionX += self.acc * self.direction
        min_x = self.startPosition + self.patrol_range[0]
        max_x = self.startPosition + self.patrol_range[1]
        if self.positionX <= min_x or self.positionX >= max_x:
            self.direction *= -1