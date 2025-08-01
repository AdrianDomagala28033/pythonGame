import random

import pygame

from gameCode.Classes.NPC.questNPC import QuestNPC
from gameCode.Classes.NPC.upgradeNPC import UpgradeNPC
from gameCode.Classes.coinClass import Coin
from gameCode.Classes.enemies.ghost import GhostEnemy
from gameCode.Classes.enemies.robugs import RobugEnemy
from gameCode.Classes.enemies.shooter import ShooterEnemy
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.levels.levelElements.chest import Chest
from gameCode.Classes.levels.levelElements.door import Door
from gameCode.Classes.levels.levelElements.key import Key
from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.Classes.playerClass import Player
from gameCode.Classes.quests.Quest import Quest
from gameCode.Classes.quests.loadFromFileQuests import loadQuestsFromFile
from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.swordClass import Sword

tileImages = [
    pygame.image.load("./images/terrain/darkBricks.png"),
    pygame.image.load("./images/terrain/meshBrick.png"),
    pygame.image.load("./images/terrain/runeBrick.png"),
]
def load_from_file(file_path, window, onLevelChange=None):
    tile_size = 50
    tiles = []
    enemies = []
    coins = []
    key = []
    door = Door(0, 0)
    chests = []
    NPCs = []
    quests = []
    player = Player(window)

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
                from gameCode.saves.saveManager import loadGame
                gameData = loadGame() or {}
                savedData = loadGame()
                if savedData:
                    data = loadGame()
                    player.coins = data["coins"]
                    player.health = data["health"]
                    player.inventory.setWeaponList(data["weaponInventory"])
                    player.inventory.setItemList(data["itemInventory"])
                if "weaponInventory" in gameData:
                    for weaponDict in gameData["weaponInventory"]:
                        if isinstance(weaponDict, dict):  # zabezpieczenie
                            weapon = createWeaponFromDict(weaponDict)
                            if weapon:
                                player.inventory.addWeapon(weapon)
                        else:
                            print("⚠️ Ostrzeżenie: weaponDict nie jest słownikiem:", weaponDict)
                player.positionX = world_x
                player.positionY = world_y
            elif char == "E":
                enemies.append(GhostEnemy(world_x, world_y, player.level))
            elif char == "R":
                enemies.append(RobugEnemy(world_x, world_y, player.level))
            elif char == "S":
                enemies.append(ShooterEnemy(world_x, world_y, 15, 100))
            elif char == "C":
                coins.append(Coin(world_x, world_y))
            elif char == "K":
                key.append(Key(world_x, world_y))
            elif char == "D":
                door = Door(world_x, world_y)
                door.onLevelChange = onLevelChange
            elif char == "c":
                chests.append(Chest(world_x, world_y, random.choice(["loot", "weapon"])))
            elif char == "Q":
                npc = QuestNPC(world_x, world_y, loadQuestsFromFile("./Classes/quests/quests.json"))
                NPCs.append(npc)
            elif char == "U":
                npc = UpgradeNPC(world_x, world_y, "./images/playerAnimation/nieUzywane/player9.png", "Mentor")
                NPCs.append(npc)

    level_width = len(lines[0].strip()) * tile_size
    level_height = len(lines) * tile_size
    level = Level(tiles, player, enemies, coins, key, door, chests, level_width, level_height, NPCs)
    return level


def load_from_text_lines(lines, window, onLevelChange=None):
    tile_size = 50
    tiles = []
    enemies = []
    coins = []
    key = []
    door = Door(0, 0)
    chests = []
    NPCs = []
    quests = []
    player = Player(window)
    enemyBuffer = []

    for y, line in enumerate(lines):
        line = line.rstrip("\n")  # nie używamy .strip()
        for x, char in enumerate(line):
            world_x = x * tile_size
            world_y = y * tile_size
            if char == "#":
                tileImage = random.choice(tileImages)
                tiles.append(Ground(world_x, world_y, tileImage))
            elif char == "G":
                tileImage = pygame.image.load("./images/terrain/ground.png")
                tiles.append(Ground(world_x, world_y, tileImage))
            elif char == "P":
                from gameCode.saves.saveManager import loadGame

                gameData = loadGame() or {}
                savedData = loadGame()
                if savedData:
                    data = loadGame()
                    player.coins = data["coins"]
                    player.health = data["health"]
                    player.inventory.setWeaponList(data["weaponInventory"])
                    player.inventory.setItemList(data["itemInventory"])
                if "weaponInventory" in gameData:
                    for weaponDict in gameData["weaponInventory"]:
                        if isinstance(weaponDict, dict):  # zabezpieczenie
                            weapon = createWeaponFromDict(weaponDict)
                            if weapon:
                                player.inventory.addWeapon(weapon)
                        else:
                            print("⚠️ Ostrzeżenie: weaponDict nie jest słownikiem:", weaponDict)
                player.positionX = world_x
                player.positionY = world_y
            elif char == "E":
                enemyBuffer.append(("E", world_x, world_y))
            elif char == "R":
                enemyBuffer.append(("R", world_x, world_y))
            elif char == "C":
                coins.append(Coin(world_x, world_y))
            elif char == "K":
                key.append(Key(world_x, world_y))
            elif char == "D":
                door = Door(world_x, world_y)
                door.onLevelChange = onLevelChange
            elif char == "c":
                chests.append(Chest(world_x, world_y, random.choice(["loot", "weapon"])))
            elif char == "Q":
                quests.append(Quest("Zabij 3 duchy", "Pozbądź się 3 upiorów w lochu", "kill", "ghost", 3))
                npc = QuestNPC(world_x, world_y, quests)
                NPCs.append(npc)
    level_width = len(lines[0].strip()) * tile_size
    level_height = len(lines) * tile_size
    level = Level(tiles, player, enemies, coins, key, door, chests, level_width, level_height, NPCs)
    level.enemyBuffer = enemyBuffer
    return level

def createWeaponFromDict(data):
    tag = data.get("tag")
    if tag == "sword":
        return Sword(
            name=data["name"],
            damage=data["damage"],
            direction=data["direction"],
            icon=data["imagePath"]
        )
    elif tag == "bow":
        return Bow(
            name=data["name"],
            damage=data["damage"],
            direction=data["direction"],
            icon=data["imagePath"]
        )
    return None
def craatePlayer():
    pass