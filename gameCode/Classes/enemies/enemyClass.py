import random

import pygame

from gameCode.Classes.coinClass import Coin
from gameCode.Classes.levels.levelElements.key import Key
from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.Classes.physicClass import Physic
import pygame
from gameCode.Classes.physicClass import Physic

class Enemy(Physic):
    def __init__(self, x, y, image, baseHealth, baseDamage, xpValue, playerLevel):
        width, height = image.get_width(), image.get_height()
        super().__init__(x, y, width, height, acc=2, maxVelocity=5)
        self.image = image
        self.baseHealth = baseHealth
        self.baseDamage = baseDamage
        self.health = baseHealth + int(playerLevel * 5)
        self.damage = baseDamage + int(playerLevel * 1.5)
        self.xpValue = xpValue
        self.direction = 1
        self.startPosition = x
        self.patrol_range = (-200, 200)
        self.visionRange = 0
        self.lastSeenPlayerTime = 0
        self.lastTriggerTime = 0
        self.state = ""
        self.lastHitTime = 0
        self.healthBarVisibleTime = 1500
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.dropTable = [
            ("coin", 0.5),
            ("health_potion", 0.3),
            ("key", 0.1)
        ]
        self.droppedItemsList = []
        self.dead = False

    def tick(self, player, obstacles, window):
        self.physicTick(player, obstacles)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)


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
        if(self.tag == "robug" and self.detectPlayer(player)):
            self.health -= damage
            self.lastHitTime = pygame.time.get_ticks()
            self.knockback(player)
        elif(self.tag != "robug"):
            self.health -= damage
            self.lastHitTime = pygame.time.get_ticks()
            self.knockback(player)
        self.knockbackTimer = 10
        self.invulnerable = True
        self.invulnerable_timer = 30
        if self.dead:
            return
        if self.health <= 0 and not self.dead:
            self.die(player)

    def knockback(self, player):
        if self.tag != "robug" and self.grounded == True:
            if self.positionX < player.positionX:
                self.horVelocity = self.knockbackForce
            else:
                self.horVelocity = -self.knockbackForce
        elif self.tag == "robug":
            if self.positionX < player.positionX:
                self.positionX -= (self.knockbackForce*4)
            else:
                self.positionX += (self.knockbackForce*4)

    def returnToStart(self):
        if abs(self.positionX - self.startPosition) < 2:
            self.positionX = self.startPosition  # dokładnie wyrównaj
            self.state = "patrol"
        else:
            self.direction = -1 if self.positionX > self.startPosition else 1
            self.positionX += self.acc * self.direction
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
    def die(self, player):
        if self.dead:
            return
        player.questManager.updateQuests("kill", "ghost")
        self.dead = True
        player.gainXP(self.xpValue)
