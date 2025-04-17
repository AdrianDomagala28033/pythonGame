import pygame
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.projectileClass import Projectile


class Bow(Projectile):
    def __init__(self, name, damage, x, y, cooldown, direction, window):
        self.name = name
        self.damage = damage
        super().__init__(x, y, direction, window)
        self.tag = "bow"
        self.cooldown = cooldown
        self.last_shot_time = 0
        self.projectiles = []

    def tick(self, window):
        pass

    def shoot(self, x, y,direction, window):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.cooldown:
            arrow = Projectile(x + 70, y,direction, window)
            self.projectiles.append(arrow)
            self.last_shot_time = now


