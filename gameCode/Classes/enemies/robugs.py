import pygame

from gameCode.Classes.enemies.enemyClass import Enemy


class RobugEnemy(Enemy):
    def __init__(self,x, y, damage, health, image=pygame.image.load("./images/enemiesAnimation/enemy.png")):
        super().__init__(x, y, image)
        self.image = pygame.transform.flip(image, True, False)
        self.damage = damage
        self.health = health
        self.tag = "robug"
        self.visionRange = 250
        self.direction = -1

    def tick(self, player, obstacles, window):
        self.physicTick(player, obstacles)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        if self.detectPlayer(player):
            self.followPlayer(player)

    def followPlayer(self, player): #jeśli odwrócę direction enemy ucieka od gracza, można wykorzystać to u innych przeciwników
        if player.positionX < self.positionX:
            self.direction = -1
        else:
            self.direction = 1
        self.positionX += self.acc * self.direction

