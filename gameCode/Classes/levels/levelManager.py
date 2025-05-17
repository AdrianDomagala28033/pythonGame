import random

import pygame

from gameCode.Classes.levels.levelClass import Level
from gameCode.Classes.levels.levelGenerator import LevelGenerator


class LevelManager():
    def __init__(self, window):
        self.window = window
        self.levels = []
        self.currentLevelIndex = -1
        self.map = ""

    def nextLevel(self):
        self.drawLoadingScreen(self.window, "Generating level...")
        pygame.display.update()
        generator = LevelGenerator()
        levelData = generator.generateLevel()

        for line in levelData:
            print(line)

        # Zamień listę list znaków na listę stringów
        text_lines = ["".join(row) for row in levelData]
        self.map = text_lines
        newLevel = Level.load_from_text_lines(text_lines, self.window)
        self.levels.append(newLevel)
        self.currentLevelIndex += 1
        return newLevel

    def getCurrentLevel(self):
        return self.levels[self.currentLevelIndex]
    def drawLoadingScreen(self, window, text="Loading..."):
        window.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 32)
        label = font.render(text, True, (255, 255, 255))
        window.blit(label, (window.get_width() // 2 - label.get_width() // 2,
                            window.get_height() // 2 - label.get_height() // 2))
        pygame.display.flip()