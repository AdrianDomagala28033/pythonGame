import pygame

from gameCode.Classes.coinClass import Coin
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemyClass import Enemy
from gameCode.Classes.playerClass import Player
from gameCode.Classes.equipment.potions import health_potion

class Level:
    def __init__(self, tiles, player, enemies, coins, width):
        self.tiles = tiles
        self.player = player
        self.enemies = enemies
        self.coins = coins
        self.levelWidth = width
        self.cameraX = 0
        tileSize = 50
        tileCount = width // tileSize
        self.levelWidth = tileSize * tileCount

    def update_camera(self):
        self.cameraX = self.player.positionX - 1280 // 2
        self.cameraX = max(0, min(self.cameraX, self.levelWidth - 1280))

    def update(self, obstacles, window):
        self.player.tickPosition(self.levelWidth)

        for enemy in self.enemies:
            enemy.tick(self.player, obstacles, window)

        selectedWeapon = self.player.inventory.getSelectedWeapon()
        if selectedWeapon and selectedWeapon.tag == "bow":
            for b in selectedWeapon.projectiles:
                 b.bulletColision(self.player, self.enemies)

    def draw(self, window):
        for tile in self.tiles:
            window.blit(tile.image, (tile.positionX - self.cameraX, tile.positionY))

        for e in self.enemies:
            e.draw(window, self.cameraX)

        for c in self.coins:
            window.blit(c.image, (c.positionX - self.cameraX, c.positionY))
            if(c.tick(self.player)):
                self.coins.remove(c)


        window.blit(
            pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {self.player.coins}", True, (0, 0, 0)), (1000, 0))
        self.player.draw(window, self.cameraX)

    @classmethod
    def load_from_file(cls, file_path, window):
        tile_size = 50
        tiles = []
        enemies = []
        coins = []
        player = None

        with open(file_path, "r") as f:
            lines = f.readlines()

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                world_x = x * tile_size
                world_y = y * tile_size
                if char == "#":
                    tileImage = pygame.image.load("./images/terrain/bricks.png")
                    tiles.append(Ground(world_x, world_y, tileImage))
                elif char == "G":
                    tileImage = pygame.image.load("./images/terrain/ground.png")
                    tiles.append(Ground(world_x, world_y, tileImage))
                elif char == "P":
                    player = Player(window)
                    player.positionX = world_x
                    player.positionY = world_y
                elif char == "E":
                    enemyImg = pygame.image.load("./images/enemiesAnimation/ghost.png")
                    enemies.append(Enemy(world_x, world_y, enemyImg, "ghost"))
                elif char == "R":
                    enemyImg = pygame.image.load("./images/enemiesAnimation/enemy.png")
                    enemies.append(Enemy(world_x, world_y, enemyImg, "enemy"))
                elif char == "C":
                    coinImg = pygame.image.load("./images/coin.png")
                    coins.append(Coin(world_x, world_y))

        level_width = len(lines[0].strip()) * tile_size
        return cls(tiles, player, enemies, coins, level_width)
