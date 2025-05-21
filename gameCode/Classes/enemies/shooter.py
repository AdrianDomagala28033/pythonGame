import pygame

from gameCode.Classes.enemies.enemyClass import Enemy
from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.projectileClass import Projectile


class ShooterEnemy(Enemy):
    def __init__(self,x, y, damage, health, image=pygame.image.load("./images/enemiesAnimation/robugAnimation/robug.png")):
        super().__init__(x, y, image)
        self.standImage = image
        self.detectImages = [pygame.image.load(f"./images/enemiesAnimation/robugAnimation/robug{x+1}.png") for x in range(6)]
        self.detectIndex = 1
        self.damage = damage
        self.health = health
        self.tag = "shooter"
        self.visionRange = 250
        self.direction = -1
        self.weapon = Bow("Basic Bow", 12, 100, self.direction, "./images/weapons/standardBow.PNG")
        self.last_shot_time = 0
    def tick(self, player, obstacles, window):
        self.shooter(self.positionX, self.positionY)
    def shooter(self,x,y):
            arrow = Projectile(x + 70, y, self.direction)
            self.weapon.projectiles.append(arrow)

