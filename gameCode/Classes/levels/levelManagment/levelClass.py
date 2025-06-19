import pygame

from gameCode.Classes.NPC.upgradeNPC import UpgradeNPC
from gameCode.Classes.enemies.ghost import GhostEnemy
from gameCode.Classes.enemies.robugs import RobugEnemy


class Level:
    def __init__(self, tiles, player, enemies, coins, key, door, chests, width, height, NPCs):
        self.tiles = tiles
        self.player = player
        self.enemies = enemies
        self.enemyBuffer = []
        self.coins = coins
        self.chests = chests
        self.NPCs = NPCs
        self.levelWidth = width
        self.levelHeight = height
        self.cameraX = 0
        self.cameraY = 0
        self.key = key
        self.door = door
        self.lastActivationCheck = 0
        tileSize = 50
        tileCountW = width // tileSize
        tileCountH = height // tileSize
        self.levelWidth = tileSize * tileCountW
        self.levelHeight = tileSize * tileCountH
        self.door.onLevelChange = None

    def update_camera(self):
        self.cameraX = self.player.positionX - 1280 // 2
        self.cameraX = max(0, min(self.cameraX, self.levelWidth - 1280))

        self.cameraY = self.player.positionY - 720 // 2
        self.cameraY = max(0, min(self.cameraY, self.levelHeight - 720))

    def update(self, obstacles, window):
        self.player.tickPosition(self.levelWidth)
        self.door.tick(self.player, window)
        self.activateEnemiesNearPlayer()
        self.cullDistantEnemies()
        for k in self.key:
            k.tick(self.player)
        for c in self.chests:
            c.tick(self.player)
        for npc in self.NPCs:
            npc.tick(self.player)
            if hasattr(npc, "handleInput") and callable(npc.handleInput):
                npc.handleInput(self.player, pygame.key.get_pressed())
        for enemy in self.enemies:
            enemy.tick(self.player, obstacles, window)
            if enemy.health <= 0:
                enemy.die(self.player)
            if enemy.dead:
                self.enemies.remove(enemy)


        selectedWeapon = self.player.inventory.getSelectedWeapon()
        if selectedWeapon and selectedWeapon.tag == "bow":
            for b in selectedWeapon.projectiles:
                 b.bulletColision(self.player, self.enemies, obstacles)

    def draw(self, window):
        for tile in self.tiles:
            window.blit(tile.image, (tile.positionX - self.cameraX, tile.positionY - self.cameraY))

        for e in self.enemies:
            e.draw(window, self.cameraX, self.cameraY)

        for c in self.coins:
            window.blit(c.image, (c.positionX - self.cameraX, c.positionY - self.cameraY))
            if(c.tick(self.player)):
                self.coins.remove(c)
        for k in self.key:
            k.draw(window, self.cameraX, self.cameraY)
        for c in self.chests:
            c.draw(window, self.cameraX, self.cameraY)
        for npc in self.NPCs:
            npc.draw(window, self.cameraX, self.cameraY, self.player)
        self.door.draw(window, self.cameraX, self.cameraY)

        self.player.draw(window, self.cameraX, self.cameraY)

    def activateEnemiesNearPlayer(self):
        px = self.player.positionX
        py = self.player.positionY
        # Dystans aktywacji — ekran + zapas
        activationRangeX = 800
        activationRangeY = 600

        for enemyData in self.enemyBuffer[:]:
            tag, x, y = enemyData
            if abs(x - px) < activationRangeX and abs(y - py) < activationRangeY:
                if tag == "E":
                    self.enemies.append(GhostEnemy(x, y, self.player.level))
                elif tag == "R":
                    self.enemies.append(RobugEnemy(x, y, self.player.level))
                self.enemyBuffer.remove(enemyData)
                if pygame.time.get_ticks() - self.lastActivationCheck < 500:
                    return
                self.lastActivationCheck = pygame.time.get_ticks()

    def cullDistantEnemies(self):
        px = self.player.positionX
        py = self.player.positionY
        maxDistance = 1400  # dopasuj do ekranu / mapy
        stillActive = []
        for enemy in self.enemies:
            ex, ey = enemy.positionX, enemy.positionY  # albo enemy.x / enemy.y
            if abs(ex - px) < maxDistance and abs(ey - py) < maxDistance:
                stillActive.append(enemy)
            else:
                # opcjonalnie: zapisz z powrotem do buffer
                if isinstance(enemy, GhostEnemy):
                    self.enemyBuffer.append(("E", ex, ey))
                elif isinstance(enemy, RobugEnemy):
                    self.enemyBuffer.append(("R", ex, ey))
        self.enemies = stillActive

