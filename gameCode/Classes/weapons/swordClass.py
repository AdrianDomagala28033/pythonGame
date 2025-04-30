import pygame
from gameCode.Classes.weapons.weapon import Weapon


class Sword(Weapon):
    def __init__(self, name, damage, cooldown, direction, icon = None):
        super().__init__(name, damage, range=100)
        self.tag = "sword"
        self.cooldown = cooldown
        self.lastAttackTime = 0
        self.direction = direction
        self.icon = icon

    def slash(self,player, enemies):
        now = pygame.time.get_ticks()
        if (now - self.lastAttackTime >= self.cooldown):
            for e in enemies:
                distance = abs(player.positionX - e.positionX)
                if distance < self.range and abs(player.positionY - e.positionY) < player.height:
                    e.takeDamage(self.damage, player)
                self.lastAttackTime = now