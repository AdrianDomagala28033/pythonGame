import pygame
from math import floor

from gameCode.Classes.UI.Inventory import Inventory
from gameCode.Classes.UI.InventoryItems.potions import health_potion
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.swordClass import Sword
from gameCode.fonts.fonts import addFont
from gameCode.saves.saveManager import saveGame, filterUsedKeys


class Player(Physic):

    def __init__(self, window):
        self.standImage = pygame.image.load(f"./images/playerAnimation/player0.png")
        width = 45
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
        self.inventory = Inventory()
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.coins = 0
        self.hasKey = False
        self.inventory.addWeapon(Sword("Basic Sword", 10, 100, self.direction, "./images/weapons/standardSword.PNG"))
        self.inventory.addWeapon(Bow("Basic Bow", 12, 100, self.direction, "./images/weapons/standardBow.PNG"))
        self.wantInteract = False


    def tick(self, keys, grounds, enemy, window):
        self.physicTick(self, grounds)
        self.enemyCollision(enemy)
        self.move(keys, window)
        self.useInventory()
        keys = pygame.key.get_pressed()
        self.handleJumpInput(keys, grounds)
        selectedWeapon = self.inventory.getSelectedWeapon()
        if selectedWeapon and selectedWeapon.tag == "sword":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                weapon = self.inventory.getSelectedWeapon()  # shoot
                if weapon.tag == "sword":
                    selectedWeapon.slash(self, enemy)
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def tickPosition(self, levelWidth):
        self.positionX = max(0, min(self.positionX, levelWidth - self.width))
    def draw(self, window, cameraX, cameraY):
        self.drawUI(window)
        self.walkAnimation(window, cameraX, cameraY)
        weapon = self.inventory.getSelectedWeapon()
        if weapon and weapon.tag == "bow":
            for proj in weapon.projectiles:
                proj.draw(window, cameraX, cameraY)


    def healthBar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (50, 5, self.width * (self.health / 100) + 4, 20))
        pygame.draw.rect(window, (235, 64, 52), (52, 7, (self.width) * (self.health / 100), 15))

    def changeDirection(self, window, cameraX, cameraY):
        if (self.direction > 0):
            window.blit(self.walkImg[floor(self.walkIndex)], (self.positionX - cameraX, self.positionY - cameraY))
        else:
            window.blit(pygame.transform.flip(self.walkImg[floor(self.walkIndex)], True, False), (self.positionX - cameraX, self.positionY - cameraY))
    def walkAnimation(self, window, cameraX, cameraY):
        if (self.jumping and self.direction > 0):
            window.blit(self.jumpImg, (self.positionX - cameraX, self.positionY - cameraY))
        elif(self.jumping and self.direction < 0):
            window.blit(pygame.transform.flip(self.jumpImg, True, False), (self.positionX - cameraX, self.positionY - cameraY))
        elif(self.horVelocity != 0):
            self.changeDirection(window, cameraX, cameraY)
            self.walkIndex += 0.3
            if self.walkIndex > 5:
                self.walkIndex = 0
        else:
            if(self.direction < 0):
                window.blit(pygame.transform.flip(self.standImage, True, False), (self.positionX - cameraX, self.positionY - cameraY))
            else:
                window.blit(self.standImage, (self.positionX - cameraX, self.positionY - cameraY))

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
        weapon = self.inventory.getSelectedWeapon()
        if weapon:
            weapon.direction = self.direction
            if(self.direction > 0):
                weapon.shoot(self.positionX - 10, self.positionY + 30)
            else:
                weapon.shoot(self.positionX - 65, self.positionY + 30)
    def move(self, keys, window):
        if (keys[pygame.K_a] and self.horVelocity > self.maxVelocity * -1):
            self.horVelocity -= self.acc
            self.direction = -1
        if (keys[pygame.K_d] and self.horVelocity < self.maxVelocity):
            self.horVelocity += self.acc
            self.direction = 1
        if(keys[pygame.K_w]):
            self.inventory.useItem(self)
        if keys[pygame.K_c]:
            weapon = self.inventory.getSelectedWeapon()# shoot
            if weapon.tag == "bow":
                self.shoot(window)
            else:
                pass
        if (keys[pygame.K_f]):
            itemList = []
            for w in self.inventory.getItemList():
                if w != None:
                    itemList.append(w)
            saveGame({
                "player_x": self.positionX,
                "player_y": self.positionY,
                "coins": self.coins,
                "weaponInventory": [w.toDict() for w in self.inventory.getWeaponList()],
                "itemInventory": [i.toDict() for i in filterUsedKeys(self.inventory.getItemList()) if i],
                "health": self.health
            })
        if (keys[pygame.K_e]): #use item
            self.wantInteract = True
        if not (keys[pygame.K_e]):
            self.wantInteract = False
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (self.horVelocity > 0):
                self.horVelocity -= self.acc
            elif(self.horVelocity < 0):
                self.horVelocity += self.acc
        if (keys[pygame.K_s]):
            self.height = 45
            self.acc = 0
        if not (keys[pygame.K_s]):
            self.height = self.standImage.get_height()
            self.acc = 0.5
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
    def drawUI(self, window):
        window.blit(pygame.image.load(f"./images/UI.png"), (10, 0))
        self.healthBar(window)
        self.inventory.drawInventory(window)
        font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf")
        textSurface = font.render(f"{self.coins}", True, (255,255,255))
        window.blit(textSurface, (50, 30))
    def interact(self):
        pass