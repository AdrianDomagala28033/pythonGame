from time import sleep

import pygame
from math import floor

from gameCode.Classes.gameObjectClass import GameObject
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.bowClass import Bow
from gameCode.Classes.projectileClass import Projectile


class Player(Physic):

    def __init__(self, window):
        self.standImage = pygame.image.load(f"./images/playerAnimation/player0.png")
        width = self.standImage.get_width()
        height = self.standImage.get_height()
        self.health = 100
        super().__init__(0, 600, width, height, 0.5, 5)
        self.jumpImg = pygame.image.load(f"./images/playerAnimation/player9.png")
        self.walkImg = [pygame.image.load(f"./images/playerAnimation/player{x}.png") for x in range(1, 7)]
        self.walkIndex = 4
        self.tag = "player"
        self.jumping = False
        self.direction = 1
        self.distanceWeapon = Bow("aa", 5,self.positionX, self.positionY,800, self.direction, window)
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.invulnerable_timer = 0


    def tick(self, keys, grounds, enemy, window):
        self.physicTick(grounds)
        self.enemyCollision(enemy)
        self.move(keys, window)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
    def draw(self, window):
        self.healthBar(window)
        self.walkAnimation(window)

    def healthBar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (3, 3, self.width + 5, 15))
        pygame.draw.rect(window, (235, 64, 52), (5, 5, (self.width) * (self.health / 100), 10))

    def changeDirection(self, window    ):
        if (self.direction > 0):
            window.blit(self.walkImg[floor(self.walkIndex)], (self.positionX, self.positionY))
        else:
            window.blit(pygame.transform.flip(self.walkImg[floor(self.walkIndex)], True, False), (self.positionX, self.positionY))
    def walkAnimation(self, window):
        if (self.jumping and self.direction > 0):
            window.blit(self.jumpImg, (self.positionX, self.positionY))
        elif(self.jumping and self.direction < 0):
            window.blit(pygame.transform.flip(self.jumpImg, True, False), (self.positionX, self.positionY))
        elif(self.horVelocity != 0):
            self.changeDirection(window)
            self.walkIndex += 0.3
            if self.walkIndex > 5:
                self.walkIndex = 0
        else:
            window.blit(self.standImage, (self.positionX, self.positionY))

    def enemyCollision(self, enemy):
        for e in enemy:
            if self.hitbox.colliderect(e.hitbox) and not self.invulnerable:
                self.health -= e.damage
                self.knockbackTimer = 10
                self.invulnerable = True
                self.invulnerable_timer = 30

                if self.positionX < e.positionX:
                    self.horVelocity = -self.knockbackForce
                else:
                    self.horVelocity = self.knockbackForce

                self.verVelocity = -5
    def shoot(self, window):
        self.distanceWeapon.tick(window)

    def move(self, keys, window):
        if (keys[pygame.K_a] and self.horVelocity > self.maxVelocity * -1):
            self.horVelocity -= self.acc
            self.direction = -1
        if (keys[pygame.K_d] and self.horVelocity < self.maxVelocity):
            self.horVelocity += self.acc
            self.direction = 1
        if(keys[pygame.K_SPACE] and self.jumping == False):
            self.verVelocity -= 15
            self.jumping = True
        if(keys[pygame.K_e]):
            self.distanceWeapon.shoot(self.positionX, self.positionY, self.direction, window)
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (self.horVelocity > 0):
                self.horVelocity -= self.acc
            elif(self.horVelocity < 0):
                self.horVelocity += self.acc