import pygame

from gameCode.Classes.coinClass import Coin
from gameCode.Classes.enemies.ghost import GhostEnemy
from gameCode.Classes.enemies.robugs import RobugEnemy
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.levels.levelElements.chest import Chest
from gameCode.Classes.levels.levelElements.door import Door
from gameCode.Classes.levels.levelElements.key import Key
from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.Classes.playerClass import Player



def load_from_file(file_path, window, onLevelChange=None):
    tile_size = 50
    tiles = []
    enemies = []
    coins = []
    key = []
    door = Door(0, 0)
    chests = []
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
                door.onLevelChange = onLevelChange
            elif char == "c":
                chests.append(Chest(world_x, world_y))

    level_width = len(lines[0].strip()) * tile_size
    level_height = len(lines) * tile_size
    level = Level(tiles, player, enemies, coins, key, door, chests, level_width, level_height)
    return level


def load_from_text_lines(lines, window, onLevelChange=None):
    tile_size = 50
    tiles = []
    enemies = []
    coins = []
    key = []
    door = Door(0, 0)
    chests = []
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
                door.onLevelChange = onLevelChange
            elif char == "c":
                chests.append(Chest(world_x, world_y))

    level_width = len(lines[0].strip()) * tile_size
    level_height = len(lines) * tile_size
    level = Level(tiles, player, enemies, coins, key, door, chests, level_width, level_height)
    return level