import pygame

from gameCode.Classes.enemies.enemyClass import Enemy


class RobugEnemy(Enemy):
    def __init__(self,x, y, damage, health, image=pygame.image.load("./images/enemiesAnimation/robugAnimation/robug.png")):
        super().__init__(x, y, image)
        self.standImage = image
        self.detectImages = [pygame.image.load(f"./images/enemiesAnimation/robugAnimation/robug{x+1}.png") for x in range(6)]
        self.detectIndex = 1
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

        self.playDetectAnimation(player)

    def followPlayer(self, player): #jeśli odwrócę direction enemy ucieka od gracza, można wykorzystać to u innych przeciwników
        if player.positionX < self.positionX:
            self.direction = -1

        else:
            self.direction = 1
            self.standImage = pygame.transform.flip(self.standImage, True, False)
        self.positionX += self.acc * self.direction
    def playDetectAnimation(self, player):
        if self.detectPlayer(player):
            self.detectIndex += 0.25
            if self.detectIndex >= len(self.detectImages):
                self.detectIndex = 0  # zapętlamy animację
        else:
            self.detectIndex = 0  # wróć do pierwszej klatki, lub: -= 0.3 aby cofać

        self.image = self.detectImages[int(self.detectIndex)]


