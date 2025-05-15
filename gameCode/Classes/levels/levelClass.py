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
        tileCount = width // tileSize
        self.levelWidth = tileSize * tileCount

    def update_camera(self):
        self.cameraX = self.player.positionX - 1280 // 2
        self.cameraX = max(0, min(self.cameraX, self.levelWidth - 1280))
        self.cameraY = self.player.positionY - 720 // 2
        self.cameraY = max(0, self.cameraY - 120)

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
        self.door.draw(window, self.cameraX, self.cameraY)

        window.blit(
            pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {self.player.coins}", True, (255, 255, 255)), (1000, 0))
        self.player.draw(window, self.cameraX, self.cameraY)

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
                    enemyImg = pygame.image.load("./images/enemiesAnimation/ghost.png")
                    enemies.append(GhostEnemy(world_x, world_y, enemyImg, "ghost"))
                elif char == "R":
                    enemyImg = pygame.image.load("./images/enemiesAnimation/enemy.png")
                    enemies.append(Enemy(world_x, world_y, enemyImg, "enemy"))
                elif char == "C":
                    coins.append(Coin(world_x, world_y))
                elif char == "K":
                    key.append(Key(world_x, world_y))
                elif char == "D":
                    door = Door(world_x, world_y)
                elif char == " ":
                    pass


        level_width = len(lines[0].strip()) * tile_size
        level_height = len(lines) * tile_size
        return cls(tiles, player, enemies, coins, key, door, level_width, level_height)

    @classmethod
    def load_from_text_lines(cls, lines, window):
        tile_size = 50
        tiles = []
        enemies = []
        ghosts = []
        coins = []
        key = []
        door = Door(0, 0)
        player = None


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