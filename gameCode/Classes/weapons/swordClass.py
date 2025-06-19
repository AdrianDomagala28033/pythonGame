import pygame

from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.Classes.weapons.weapon import Weapon


class Sword(Weapon):
    def __init__(self, name, damage, cooldown, direction, icon = None):
        super().__init__(name, damage, icon, value=0, range=100)
        self.tag = "sword"
        self.cooldown = cooldown
        self.lastAttackTime = 0
        self.direction = direction
        self.icon = icon
        self.upgradeLevel = 0

    def slash(self,player, enemies):
        now = pygame.time.get_ticks()
        if (now - self.lastAttackTime >= self.cooldown):
            for e in enemies:
                distance = abs(player.positionX - e.positionX)
                if distance < self.range and abs(player.positionY - e.positionY) < player.height:
                    baseDamage = self.getEffectiveDamage(player.level)
                    bonus = player.strength * 1  # każdy punkt siły = +1 dmg (albo więcej)
                    e.takeDamage(baseDamage + bonus, player)
                self.lastAttackTime = now
    def toDict(self):
        return {
            "tag": "sword",
            "name": self.name,
            "damage": self.damage,
            "cooldown": self.cooldown,
            "direction": self.direction,
            "icon": self.icon
        }
    def enemyInRange(self, player, enemy):
        distance = abs(player.positionX - enemy.positionX)
        vertical = abs(player.positionY - enemy.positionY)
        return distance < self.range and vertical < player.height