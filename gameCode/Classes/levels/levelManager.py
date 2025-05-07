from gameCode.Classes.levels.levelClass import Level
from gameCode.Classes.levels.levelGenerator import LevelGenerator


class LevelManager():
    def __init__(self, window):
        self.window = window
        self.levels = []
        self.currentLevelIndex = -1

    def nextLevel(self):
        generator = LevelGenerator()
        level_data = generator.generatePassableLevelText()
        newLevel = Level.load_from_text_lines(level_data, self.window)
        self.levels.append(newLevel)
        self.currentLevelIndex += 1
        return newLevel

    def getCurrentLevel(self):
        return self.levels[self.currentLevelIndex]