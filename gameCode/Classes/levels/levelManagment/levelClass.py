import pygame

class Level:
    def __init__(self, tiles, player, enemies, coins, key, door, chests, width, height):
        self.tiles = tiles
        self.player = player
        self.enemies = enemies
        self.coins = coins
        self.chests = chests
        self.levelWidth = width
        self.levelHeight = height
        self.cameraX = 0
        self.cameraY = 0
        self.key = key
        self.door = door
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
        for k in self.key:
            k.tick(self.player)
        for c in self.chests:
            c.tick(self.player)
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
        self.door.draw(window, self.cameraX, self.cameraY)

        self.player.draw(window, self.cameraX, self.cameraY)




