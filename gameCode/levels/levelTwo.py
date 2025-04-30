import pygame
import sys

from gameCode.Classes.levels.levelClass import Level  # Upewnij się że ścieżka jest prawidłowa

# Inicjalizacja Pygame
pygame.init()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dungeon Escape - Test")
clock = pygame.time.Clock()

def levelTwo(window):
    # Załaduj poziom
    try:
        level = Level.load_from_file("levels/levelsTXT/levelTwo.txt", window)
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
        level.player.tick(keys, level.tiles, level.enemies, [], window)
        # level.enemies[0].tick(level.player)
        level.update_camera()
        level.update(level.tiles, window)

        # Rysowanie
        window.fill((30, 30, 30))
        level.draw(window)
        pygame.display.flip()

    # Zamykanie Pygame
    pygame.quit()
    sys.exit()