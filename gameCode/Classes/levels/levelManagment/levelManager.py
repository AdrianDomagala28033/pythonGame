import pygame

from gameCode.Classes.levels.levelManagment.generator.newGenerator.newLevelGenerator import generateLevel, \
    generateOpenLevel, generateDeadCellsStyleLevel, generateNaturalModularLevel
from gameCode.Classes.levels.levelManagment.levelLoading import load_from_text_lines
from gameCode.saves.saveManager import saveGame, filterUsedKeys


class LevelManager():
    def __init__(self, window):
        self.window = window
        self.levels = []
        self.currentLevelIndex = -1
        self.map = ""

    def nextLevel(self):
        print("Wywołanie")
        currentLevel = self.getCurrentLevel() if self.currentLevelIndex >= 0 else None
        if currentLevel and currentLevel.player:
            player = currentLevel.player
            saveGame({
                "player_x": player.positionX,
                "player_y": player.positionY,
                "coins": player.coins,
                "weaponInventory": [w.toDict() for w in player.inventory.getWeaponList()],
                "itemInventory": [i.toDict() for i in filterUsedKeys(player.inventory.getItemList()) if i],
                "health": player.health
            })
            print("Zapisano grę przed zmianą poziomu.")
        pygame.display.update()

        levelLines = generateNaturalModularLevel()
        newLevel = load_from_text_lines(levelLines, self.window, onLevelChange=self.nextLevel)
        newLevel.door.onLevelChange = self.nextLevel
        self.map = levelLines
        self.levels.append(newLevel)
        self.currentLevelIndex += 1
        return newLevel

    def getCurrentLevel(self):
        return self.levels[self.currentLevelIndex]
