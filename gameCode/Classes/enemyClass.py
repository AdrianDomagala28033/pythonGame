import pygame

from gameCode.Classes.physicClass import Physic
import pygame
from gameCode.Classes.physicClass import Physic

class Enemy(Physic):
    def __init__(self, x, y, image, tag, ai_type="patrol"):
        width, height = image.get_width(), image.get_height()
        super().__init__(x, y, width, height, acc=2, maxVelocity=5)
        self.image = image
        self.health = 100
        self.damage = 10
        self.direction = 1
        self.startPosition = x
        self.patrol_range = (-200, 200)
        self.visionRange = 100
        self.lastSeenPlayerTime = 0
        self.lastTriggerTime = 0
        self.ai_type = ai_type
        self.state = "patrol"
        self.lastHitTime = 0
        self.healthBarVisibleTime = 1500
        self.tag = tag
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self, player, obstacles, window):
        self.physicTick(player, obstacles)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.enemyType(player)

    def enemyType(self, player):
        if(self.tag == "ghost"):
            self.handleAi(player)
        elif(self.tag == "enemy"):
            self.visionRange = 300
            self.waitForPlayer(player)

    def handleAi(self, player):
        if self.state == "patrol":
            self.patrol()
        elif self.state == "follow":
            self.followPlayer(player)
        elif self.state == "returning":
            self.returnToStart()
        elif self.state == "waiting":
            print("waiting")
            self.acc = 0

    def patrol(self):
        self.positionX += self.acc * self.direction
        min_x = self.startPosition + self.patrol_range[0]
        max_x = self.startPosition + self.patrol_range[1]
        if self.positionX <= min_x or self.positionX >= max_x:
            self.direction *= -1

    def followPlayer(self, player):
        if player.positionX < self.positionX:
            self.direction = -1
        else:
            self.direction = 1
        self.positionX += self.acc * self.direction

    def draw(self, window, cameraX, cameraY):
        self.drawImage(window, cameraX, cameraY)
        self.drawHealthbar(window, cameraX, cameraY)

    def drawImage(self, window, cameraX, cameraY):
        drawX = self.positionX - cameraX
        if self.direction < 0:
            window.blit(self.image, (drawX, self.positionY - cameraY))
        else:
            flipped = pygame.transform.flip(self.image, True, False)
            window.blit(flipped, (drawX, self.positionY - cameraY))

    def drawHealthbar(self, window, cameraX, cameraY):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastHitTime <= self.healthBarVisibleTime:
            pygame.draw.rect(window, (235, 64, 52),(self.positionX - cameraX, self.positionY - 10 - cameraY, self.width * (self.health / 100), 10))

    def takeDamage(self, damage, player):
        if(self.tag == "enemy" and self.detectPlayer(player)):
            self.health -= damage
            self.lastHitTime = pygame.time.get_ticks()
        elif self.tag == "ghost":
            self.health -= damage
            self.lastHitTime = pygame.time.get_ticks()
        self.knockbackTimer = 10
        self.invulnerable = True
        self.invulnerable_timer = 30
        self.knockback(player)

    def knockback(self, player):
        if self.tag == "ghost" and self.grounded == True:
            if self.positionX < player.positionX:
                self.horVelocity = self.knockbackForce
            else:
                self.horVelocity = -self.knockbackForce
        elif self.tag == "enemy":
            if self.positionX < player.positionX:
                self.positionX -= (self.knockbackForce*4)
            else:
                self.positionX += (self.knockbackForce*4)



    def detectPlayer(self, player, window=None, cameraX=0, cameraY=0,debug=True):
        rightVision = pygame.Rect(self.positionX, self.positionY, self.visionRange, self.height)
        leftVision = pygame.Rect(self.positionX - self.visionRange, self.positionY, self.visionRange, self.height)

        if debug and window:
            pygame.draw.rect(window, (255, 0, 0),
                             (rightVision.x - cameraX, rightVision.y - cameraY, rightVision.width, rightVision.height), 2)
            pygame.draw.rect(window, (0, 255, 0),
                             (leftVision.x - cameraX, leftVision.y- cameraY, leftVision.width, leftVision.height), 2)

        if rightVision.colliderect(player.hitbox) or leftVision.colliderect(player.hitbox):
            self.state = "follow"
            self.lastSeenPlayerTime = pygame.time.get_ticks()
            return True
        else:
            if self.state == "follow" and pygame.time.get_ticks() - self.lastSeenPlayerTime > 1000:
                self.state = "returning"

    def returnToStart(self):
        if abs(self.positionX - self.startPosition) < 2:
            self.positionX = self.startPosition  # dokładnie wyrównaj
            self.state = "patrol"
        else:
            self.direction = -1 if self.positionX > self.startPosition else 1
            self.positionX += self.acc * self.direction
    def waitForPlayer(self, player):
        self.state = "waiting"
        if self.detectPlayer(player):
            self.followPlayer(player)