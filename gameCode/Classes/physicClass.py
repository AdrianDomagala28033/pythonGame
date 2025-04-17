import pygame
from gameCode.Classes.gameObjectClass import GameObject
class Physic(GameObject):
    def __init__(self,x, y, width, height, acc, maxVelocity):

        self.verVelocity = 0
        self.horVelocity = 0
        self.acc = acc
        self.maxVelocity = maxVelocity
        self.previousX = x
        self.previousY = y
        self.jumping = False
        super().__init__(x, y, width, height)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def physicTick(self, obstacles):
        if(self.tag == "player"):
            self.movement(obstacles)
            if self.knockbackTimer > 0:
                self.knockbackTimer -= 1
        elif(self.tag == "enemy"):
            if self.hitbox.colliderect(obstacles.hitbox):
                if self.horVelocity > 0:  # poruszamy się w prawo
                    self.positionX = obstacles.hitbox.left - self.width
                elif self.horVelocity < 0:  # w lewo
                    self.positionX = obstacles.hitbox.right
                self.horVelocity = 0
                self.hitbox.x = self.positionX

    def movement(self, obstacles):
        gravity = 0.7
        self.verVelocity += gravity
        # Oś X
        self.positionX += self.horVelocity
        self.hitbox.x = self.positionX
        for obj in obstacles:
            if self.hitbox.colliderect(obj.hitbox):
                if self.horVelocity > 0:  # poruszamy się w prawo
                    self.positionX = obj.hitbox.left - self.width
                elif self.horVelocity < 0:  # w lewo
                    self.positionX = obj.hitbox.right
                self.horVelocity = 0
                self.hitbox.x = self.positionX

        # Oś Y
        self.positionY += self.verVelocity
        self.hitbox.y = self.positionY

        for obj in obstacles:
            if self.hitbox.colliderect(obj.hitbox):
                if self.verVelocity > 0:  # spadanie
                    self.positionY = obj.hitbox.top - self.height
                    self.jumping = False
                elif self.verVelocity < 0:  # skok w górę
                    self.positionY = obj.hitbox.bottom
                self.verVelocity = 0
                self.hitbox.y = self.positionY
