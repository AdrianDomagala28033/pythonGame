import pygame
from math import floor

from gameCode.Classes.UI.Inventory import Inventory
from gameCode.Classes.physicClass import Physic
from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.swordClass import Sword
from gameCode.fonts.fonts import addFont
from gameCode.images.animations import load_animation_frames, load_single_frame, scaleAnimationFrames
from gameCode.levels.gameOver import gameOver
from gameCode.saves.saveManager import saveGame, filterUsedKeys

class Player(Physic):

    def __init__(self, window):
        # === ANIMACJE ===
        self.image = pygame.transform.scale2x(load_single_frame("./images/playerAnimation/walkingCharacter.png", 21, 32, frame_index=2))
        self.standImages = scaleAnimationFrames(load_animation_frames(
            "./images/playerAnimation/idleCharacter.png", frame_width=19, frame_height=30, rows=1))
        self.jumpImg = pygame.image.load("./images/playerAnimation/jumpingCharacter.png")
        self.walkImg = [pygame.image.load(f"./images/playerAnimation/walkCharacter{x}.png") for x in range(1, 7)]

        # === STATYSTYKI ===
        self.maxHealth = 100
        self.health = self.maxHealth
        self.coins = 0
        self.hasKey = False
        self.level = 1
        self.xp = 0
        self.xpToNextLevel = 100
        self.statBoostPerLevel = {
            'health' : 10,
            'damage' : 1
        }

        # === POZYCJA / FIZYKA ===
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(0, 600, width, height, 0.5, 5)
        self.direction = 1
        self.jumping = False
        self.knockbackTimer = 0
        self.knockbackForce = 10
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.wantInteract = False

        # === INWENTARZ ===
        self.inventory = Inventory()
        self.inventory.addWeapon(Sword("Basic Sword", 10, 100, self.direction, "./images/weapons/standardSword.PNG"))
        self.inventory.addWeapon(Bow("Basic Bow", 12, 500, self.direction, "./images/weapons/standardBow.PNG"))

        # === ANIMACJE ===
        self.walkIndex = 0
        self.jumpIndex = 0
        self.standIndex = 0

        # === MISC ===
        self.tag = "player"
        self.lastAutosaveTime = pygame.time.get_ticks()
        self.autosaveInterval = 500


    # === GŁÓWNY TICK ===
    def tick(self, keys, grounds, enemies, window):
        self.physicTick(self, grounds)
        self.enemyCollision(enemies)
        self.move(keys, window)
        self.useInventory()
        self.handleJumpInput(keys, grounds)

        selectedWeapon = self.inventory.getSelectedWeapon()
        if selectedWeapon and selectedWeapon.tag == "sword" and keys[pygame.K_q]:
            selectedWeapon.slash(self, enemies)

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        if self.health <= 0:
            gameOver(window)


    # === RUCH ===
    def move(self, keys, window):
        if keys[pygame.K_a]:
            self.horVelocity = max(self.horVelocity - self.acc, -self.maxVelocity)
            self.direction = -1
        if keys[pygame.K_d]:
            self.horVelocity = min(self.horVelocity + self.acc, self.maxVelocity)
            self.direction = 1

        if keys[pygame.K_w]:
            self.inventory.useItem(self)

        if keys[pygame.K_c]:
            weapon = self.inventory.getSelectedWeapon()
            if weapon.tag == "bow":
                self.shoot(window)
                weapon.tick(window)

        self.wantInteract = keys[pygame.K_e]

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.horVelocity *= 0.9

        if keys[pygame.K_s]:
            self.height = 45
            self.acc = 0
        else:
            self.height = self.image.get_height()
            self.acc = 0.5


    # === KOLIZJA Z WROGAMI ===
    def enemyCollision(self, enemies):
        for e in enemies:
            if self.hitbox.colliderect(e.hitbox) and not self.invulnerable:
                self.health -= e.damage
                self.knockbackTimer = 10
                self.invulnerable = True
                self.invulnerable_timer = 30

                self.horVelocity = -self.knockbackForce if self.positionX < e.positionX else self.knockbackForce
                self.verVelocity = -5


    # === STRZELANIE / MIECZ ===
    def shoot(self, window):
        weapon = self.inventory.getSelectedWeapon()
        if weapon:
            weapon.direction = self.direction
            x_offset = -10 if self.direction > 0 else -65
            weapon.shoot(self.positionX + x_offset, self.positionY + 30)


    # === RYSOWANIE ===
    def draw(self, window, cameraX=0, cameraY=0):
        self.drawUI(window)
        self.walkAnimation(window, cameraX, cameraY)
        weapon = self.inventory.getSelectedWeapon()
        if weapon and weapon.tag == "bow":
            for proj in weapon.projectiles:
                proj.draw(window, cameraX, cameraY)

    def drawUI(self, window):
        window.blit(pygame.image.load(f"./images/UI.png"), (10, 0))
        self.healthBar(window)
        self.inventory.drawInventory(window)
        font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 48)
        textSurface = font.render(f"{self.coins}", True, (255,255,255))
        levelSurface = font.render(f"Poziom postaci: {self.level}", True, (255,255,255))
        window.blit(textSurface, (50, 30))
        window.blit(levelSurface, (550, 30))

    def walkAnimation(self, window, cameraX, cameraY):
        if self.jumping and self.direction > 0 and self.grounded and self.verVelocity != 0:
            img = pygame.transform.scale2x(self.jumpImg)
        elif self.jumping and self.direction < 0 and self.verVelocity != 0:
            img = pygame.transform.flip(pygame.transform.scale2x(self.jumpImg), True, False)
        elif self.horVelocity != 0:
            self.changeDirection(window, cameraX, cameraY)
            self.walkIndex = (self.walkIndex + 0.15) % len(self.walkImg)
            return
        else:
            self.standIndex = (self.standIndex + 0.1) % len(self.standImages)
            img = self.standImages[floor(self.standIndex)]
            if self.direction < 0:
                img = pygame.transform.flip(img, True, False)
        window.blit(img, (self.positionX - cameraX, self.positionY - cameraY))

    def changeDirection(self, window, cameraX, cameraY):
        image = pygame.transform.scale2x(self.walkImg[floor(self.walkIndex)])
        if self.direction < 0:
            image = pygame.transform.flip(image, True, False)
        window.blit(image, (self.positionX - cameraX, self.positionY - cameraY))

    def healthBar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (50, 5, self.width + 4, 20))
        pygame.draw.rect(window, (235, 64, 52), (52, 7, self.width * (self.health / self.maxHealth), 15))


    # === INVENTORY SELEKCJA ===
    def useInventory(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: self.inventory.selectedItemIndex = 0
        if keys[pygame.K_2]: self.inventory.selectedItemIndex = 1
        if keys[pygame.K_3]: self.inventory.selectedItemIndex = 2
        if keys[pygame.K_4]: self.inventory.selectedItemIndex = 3
        if keys[pygame.K_5]: self.inventory.selectedWeaponIndex = 0
        if keys[pygame.K_6]: self.inventory.selectedWeaponIndex = 1


    # === AUTOSAVE ===
    def performAutosave(self):
        print("Autosave")
        itemList = [i for i in filterUsedKeys(self.inventory.getItemList()) if i]
        saveGame({
            "player_x": self.positionX,
            "player_y": self.positionY,
            "coins": self.coins,
            "weaponInventory": [w.toDict() for w in self.inventory.getWeaponList()],
            "itemInventory": [i.toDict() for i in itemList],
            "health": self.health
        })

    def interact(self):
        pass

    def tickPosition(self, levelWidth):
        self.positionX = max(0, min(self.positionX, levelWidth - self.width))

    # === LEVEL UP ===
    def gainXP(self, amount):
        self.xp += amount
        print(f'Zdobyto {amount}xp na {self.xpToNextLevel}')
        while self.xp >= self.xpToNextLevel:
            self.xp -= self.xpToNextLevel
            self.levelUp()
    def levelUp(self):
        self.level += 1
        self.maxHealth += self.statBoostPerLevel['health']
        self.health = self.maxHealth
        self.xpToNextLevel = int(self.xpToNextLevel * 1.2)