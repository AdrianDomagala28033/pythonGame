import pygame
from gameCode.Classes.weapons.projectileClass import Projectile
from gameCode.Classes.weapons.weapon import Weapon


class Bow(Weapon):
    def __init__(self, name, damage, cooldown, direction, icon=None):
        super().__init__(name, damage, icon, value=0, range=0)
        self.icon = icon
        self.tag = "bow"
        self.cooldown = cooldown
        self.last_shot_time = 0
        self.projectiles = []
        self.direction = direction

    def tick(self, window):
        pass

    def shoot(self, x, y):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.cooldown:
            arrow = Projectile(x + 70, y, self.direction)
            self.projectiles.append(arrow)
            self.last_shot_time = now


