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
        self.maxJumps = 2
        self.jumpCount = self.maxJumps
        self.jumpForce = -20
        self.wallJumpForceX = 7
        self.lastJump = 0
        super().__init__(x, y, width, height)
        self.grounded = True
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def physicTick(self,player, obstacles):
        if(self.tag == "player"):
            self.movementX(obstacles)
            self.movementY(obstacles)
            if self.knockbackTimer > 0:
                self.knockbackTimer -= 1
        elif(self.tag == "ghost"):
            self.movementX(obstacles)
            self.checkBlockUnder(obstacles)
            if self.hitbox.colliderect(player.hitbox):
                if self.horVelocity > 0:  # poruszamy się w prawo
                    self.positionX = obstacles.hitbox.left - self.width
                elif self.horVelocity < 0:  # w lewo
                    self.positionX = obstacles.hitbox.right
                self.horVelocity = 0
                self.hitbox.x = self.positionX
        elif(self.tag == "robug"):
            self.movementX(obstacles)
            self.movementY(obstacles)
            self.checkBlockUnder(obstacles)

    def movementX(self, obstacles):
        gravity = 0.7
        self.verVelocity += gravity
        # Oś X
        self.positionX += self.horVelocity
        self.hitbox.x = self.positionX

        for obj in obstacles:
            if self.hitbox.colliderect(obj.hitbox):
                if self.horVelocity > 0:  # poruszamy się w prawo
                    self.positionX = obj.hitbox.left - self.width
                    self.horVelocity = 0
                    self.hitbox.x = self.positionX
                elif self.horVelocity < 0:  # w lewo
                    self.positionX = obj.hitbox.right
                    self.horVelocity = 0
                    self.hitbox.x = self.positionX

    def movementY(self, obstacles):
        gravity = 0.6
        self.verVelocity += gravity
        self.positionY += self.verVelocity
        self.hitbox.y = self.positionY

        for obj in obstacles:
            if self.hitbox.colliderect(obj.hitbox):
                if self.verVelocity > 0:
                    self.positionY = obj.hitbox.top - self.height
                    self.verVelocity = 0
                    self.jumpCount = self.maxJumps
                elif self.verVelocity < 0:
                    self.positionY = obj.hitbox.bottom
                    self.verVelocity = 0

                self.hitbox.y = self.positionY
    def checkBlockUnder(self, obstacles):
        foot_check_x = self.hitbox.midbottom[0] + (self.direction * self.width // 2)
        foot_check_y = self.hitbox.midbottom[1] + 5  # lekko pod nogami
        self.grounded = False
        for obj in obstacles:
            if obj.hitbox.collidepoint(foot_check_x, foot_check_y):
                self.grounded = True
                break

        if not self.grounded:
            self.direction *= -1
            if not self.grounded:
                self.positionX += 1

    def jump(self):
        self.verVelocity = self.jumpForce
        self.jumpCount -= 1

    def checkWallContact(self, obstacles):
        touchingLeft = False
        touchingRight = False

        for obj in obstacles:
            if self.hitbox.colliderect(obj.hitbox):
                if abs(self.hitbox.left - obj.hitbox.right) < 5:
                    touchingLeft = True
                elif abs(self.hitbox.right - obj.hitbox.left) < 5:
                    touchingRight = True

        return touchingLeft, touchingRight

    def handleJumpInput(self, keys, obstacles):
        touchingLeft, touchingRight = self.checkWallContact(obstacles)

        # Zabezpieczenie przed trzymaniem spacji
        if keys[pygame.K_SPACE]:
            if not self.jumping and self.jumpCount > 0:
                if touchingLeft:
                    self.horVelocity = self.wallJumpForceX
                elif touchingRight:
                    self.horVelocity = -self.wallJumpForceX
                self.jump()
                self.jumping = True
        else:
            self.jumping = False