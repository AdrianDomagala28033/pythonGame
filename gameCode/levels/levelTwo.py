import pygame
import sys

from gameCode.Classes.levels.levelClass import Level
from gameCode.Classes.levels.levelManager import LevelManager

# Inicjalizacja Pygame
pygame.init()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("The last exit - test")
clock = pygame.time.Clock()

def levelTwo(window):
    # Załaduj poziom
    try:
        # levelElements = Level.load_from_file("levels/levelsTXT/levelThree.txt", window)
        level = LevelManager(window)
        level.nextLevel()
        levelElements = level.getCurrentLevel()
        print("Poziom załadowany pomyślnie!")
    except Exception as e:
        print("Błąd podczas ładowania poziomu:", e)
        pygame.quit()
        sys.exit()

    # Główna pętla gry
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obsługa klawiszy
        keys = pygame.key.get_pressed()


        # Aktualizacja logiki
        levelElements.player.tick(keys, levelElements.tiles, levelElements.enemies, [], window_width, window_height)
        # level.enemies[0].tick(level.player)
        levelElements.update_camera()
        levelElements.update(levelElements.tiles, window)

        # Rysowanie
        window.fill((30, 30, 30))
        levelElements.draw(window, level.map, levelElements.player)
        pygame.display.flip()

    # Zamykanie Pygame
    pygame.quit()
    sys.exit()