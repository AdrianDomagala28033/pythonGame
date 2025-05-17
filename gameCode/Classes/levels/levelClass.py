import pygame

from gameCode.Classes.coinClass import Coin
from gameCode.Classes.enemies.ghost import GhostEnemy
from gameCode.Classes.enemies.robugs import RobugEnemy
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemies.enemyClass import Enemy
from gameCode.Classes.levels.door import Door
from gameCode.Classes.levels.key import Key
from gameCode.Classes.playerClass import Player


class Level:
    def __init__(self, tiles, player, enemies, coins, key, door, width, height):
        self.tiles = tiles
        self.player = player
        self.enemies = enemies
        self.coins = coins
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

    def update_camera(self):
        self.cameraX = self.player.positionX - 1280 // 2
        self.cameraX = max(0, min(self.cameraX, self.levelWidth - 1280))

        self.cameraY = self.player.positionY - 720 // 2
        self.cameraY = max(0, min(self.cameraY, self.levelHeight - 720))

    def update(self, obstacles, window):
        self.player.tickPosition(self.levelWidth)
        self.door.tick(self.player)
        for k in self.key:
            k.tick(self.player)

        for enemy in self.enemies:
            enemy.tick(self.player, obstacles, window)

        selectedWeapon = self.player.inventory.getSelectedWeapon()
        if selectedWeapon and selectedWeapon.tag == "bow":
            for b in selectedWeapon.projectiles:
                 b.bulletColision(self.player, self.enemies)

    def draw(self, window, levelData, player):
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
        self.door.draw(window, self.cameraX, self.cameraY)

        window.blit(
            pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {self.player.coins}", True, (255, 255, 255)), (1000, 0))
        self.player.draw(window, self.cameraX, self.cameraY)
        self.drawMiniMap(window, levelData, player, (self.cameraX, self.cameraY))
    @classmethod
    def load_from_file(cls, file_path, window):
        tile_size = 50
        tiles = []
        enemies = []
        coins = []
        key = []
        door = Door(0, 0)
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
                    enemies.append(GhostEnemy(world_x, world_y, 50, 100))
                elif char == "R":
                    enemies.append(RobugEnemy(world_x, world_y, 10, 100))
                elif char == "C":
                    coins.append(Coin(world_x, world_y))
                elif char == "K":
                    key.append(Key(world_x, world_y))
                elif char == "D":
                    door = Door(world_x, world_y)


        level_width = len(lines[0].strip()) * tile_size
        level_height = len(lines) * tile_size
        return cls(tiles, player, enemies, coins, key, door, level_width, level_height)

    @classmethod
    def load_from_text_lines(cls, lines, window):
        tile_size = 50
        tiles = []
        enemies = []
        coins = []
        key = []
        door = Door(0, 0)
        player = None


        for y, line in enumerate(lines):
            line = line.rstrip("\n")  # nie używamy .strip()
            for x, char in enumerate(line):
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
                    enemies.append(GhostEnemy(world_x, world_y, 50, 100))
                elif char == "R":
                    enemies.append(RobugEnemy(world_x, world_y, 10, 100))
                elif char == "C":
                    coins.append(Coin(world_x, world_y))
                elif char == "K":
                    key.append(Key(world_x, world_y))
                elif char == "D":
                    door = Door(world_x, world_y)


        level_width = len(lines[0].strip()) * tile_size
        level_height = len(lines) * tile_size
        return cls(tiles, player, enemies, coins, key, door, level_width, level_height)

    def drawMiniMap(self, window, levelData, player, cameraScroll, tileSize=4, topRight=(1280, 0)):

        TILE_SIZE = 50  # zakładamy kafelek 32x32

        mapWidth = len(levelData[0])
        topLeftX = topRight[0] - mapWidth * tileSize
        topLeftY = topRight[1]

        for y, row in enumerate(levelData):
            for x, cell in enumerate(row):
                color = (0, 0, 0)
                if cell == "#":
                    color = (50, 50, 50)
                elif cell == ".":
                    color = (150, 150, 150)
                elif cell == "D":
                    color = (255, 255, 0)
                elif cell == "K":
                    color = (0, 255, 255)
                elif cell == "C":
                    color = (255, 215, 0)
                elif cell in ("E", "R"):
                    color = (255, 0, 0)
                elif cell in ("T", "B"):
                    color = (100, 80, 40)

                rect = pygame.Rect(topLeftX + x * tileSize,
                                   topLeftY + y * tileSize,
                                   tileSize, tileSize)
                pygame.draw.rect(window, color, rect)

        # Uwzględnij scroll kamery
        globalX, globalY = player.hitbox.center

        gridX = int(globalX // TILE_SIZE)
        gridY = int(globalY // TILE_SIZE)

        if 0 <= gridY < len(levelData) and 0 <= gridX < len(levelData[0]):
            px = topLeftX + gridX * tileSize
            py = topLeftY + gridY * tileSize
            pygame.draw.rect(window, (0, 255, 0), (px, py, tileSize, tileSize))
