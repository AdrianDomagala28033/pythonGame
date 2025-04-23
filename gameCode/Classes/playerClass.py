import pygame
from math import floor

from gameCode.Classes.equipment.Inventory import Inventory
from gameCode.Classes.equipment.potions import health_potion
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.weapons.bowClass import Bow


class Player(Physic):

    def __init__(self, window):
        self.standImage = pygame.image.load(f"./images/playerAnimation/player0.png")
        width = self.standImage.get_width()
        height = self.standImage.get_height()
        self.maxHealth = 100
        self.health = self.maxHealth
        super().__init__(0, 600, width, height, 0.5, 5)
        self.jumpImg = pygame.image.load(f"./images/playerAnimation/player9.png")
        self.walkImg = [pygame.image.load(f"./images/playerAnimation/player{x}.png") for x in range(1, 7)]
        self.walkIndex = 4
        self.tag = "player"
        self.jumping = False
        self.direction = 1
        self.distanceWeapon = Bow("aa", 12,self.positionX, self.positionY,800, self.direction, window)
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.coins = 0
        self.inventory = Inventory()


    def tick(self, keys, grounds, enemy, window, cameraX):
        self.physicTick(self, grounds)
        self.enemyCollision(enemy)
        self.move(keys, window, cameraX)
        self.useInventory()
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def tickPosition(self, levelWidth):
        self.positionX = max(0, min(self.positionX, levelWidth - self.width))
    def draw(self, window, cameraX):
        self.healthBar(window)
        self.walkAnimation(window, cameraX)
        self.inventory.drawInventory(window)


    def healthBar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (3, 3, self.width + 5, 15))
        pygame.draw.rect(window, (235, 64, 52), (5, 5, (self.width) * (self.health / 100), 10))

    def changeDirection(self, window, cameraX):
        if (self.direction > 0):
            window.blit(self.walkImg[floor(self.walkIndex)], (self.positionX - cameraX, self.positionY))
        else:
            window.blit(pygame.transform.flip(self.walkImg[floor(self.walkIndex)], True, False), (self.positionX - cameraX, self.positionY))
    def walkAnimation(self, window, cameraX):
        if (self.jumping and self.direction > 0):
            window.blit(self.jumpImg, (self.positionX - cameraX, self.positionY))
        elif(self.jumping and self.direction < 0):
            window.blit(pygame.transform.flip(self.jumpImg, True, False), (self.positionX - cameraX, self.positionY))
        elif(self.horVelocity != 0):
            self.changeDirection(window, cameraX)
            self.walkIndex += 0.3
            if self.walkIndex > 5:
                self.walkIndex = 0
        else:
            window.blit(self.standImage, (self.positionX - cameraX, self.positionY))

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

    def move(self, keys, window, cameraX):
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
            self.inventory.useItem(self)
            self.distanceWeapon.shoot(self.positionX, self.positionY, self.direction, window)
        if (keys[pygame.K_f]):
            self.inventory.addItem(health_potion)
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (self.horVelocity > 0):
                self.horVelocity -= self.acc
            elif(self.horVelocity < 0):
                self.horVelocity += self.acc

    def useInventory(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.inventory.selectedItemIndex = 0
        elif keys[pygame.K_2]:
            self.inventory.selectedItemIndex = 1
        elif keys[pygame.K_3]:
            self.inventory.selectedItemIndex = 2
        elif keys[pygame.K_4]:
            self.inventory.selectedItemIndex = 3
        elif keys[pygame.K_5]:
            self.inventory.selectedWeaponIndex = 0
        elif keys[pygame.K_6]:
            self.inventory.selectedWeaponIndex = 1