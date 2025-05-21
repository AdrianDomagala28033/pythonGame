import pygame


from gameCode.Classes.levels.levelManagment.levelGenerator import generate_cave_with_floors, generate_normal_level, \
    generate_single_cave_level, populateLevel
from gameCode.Classes.levels.levelManagment.levelLoading import load_from_text_lines
from gameCode.saves.saveManager import loadGame, saveGame, filterUsedKeys


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
        level = generate_single_cave_level()
        levelData = populateLevel(level)

        # for line in levelData:
        #     print(line)

        # Zamień listę list znaków na listę stringów
        text_lines = ["".join(row) for row in levelData]
        for p in text_lines:
            print(p)
        self.map = text_lines
        newLevel = load_from_text_lines(text_lines, self.window, onLevelChange=self.nextLevel)

        newLevel.door.onLevelChange = self.nextLevel
        self.levels.append(newLevel)
        self.currentLevelIndex += 1
        return newLevel

    def getCurrentLevel(self):
        return self.levels[self.currentLevelIndex]
