import random

import pygame


from gameCode.Classes.levels.levelGenerator import generate_single_cave_level, generate_cave_with_floors
from gameCode.Classes.levels.levelLoading import load_from_text_lines


class LevelManager():
    def __init__(self, window):
        self.window = window
        self.levels = []
        self.currentLevelIndex = -1
        self.map = ""

    def nextLevel(self):
        print("Wywołanie")
        pygame.display.update()
        levelData = generate_cave_with_floors()

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
