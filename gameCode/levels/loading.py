import sys

import pygame

pygame.init()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("The last exit - test")

def drawLoadingScreen(window, text="Loading..."):
    window.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 32)
    label = font.render(text, True, (255, 255, 255))
    window.blit(label, (window.get_width() // 2 - label.get_width() // 2,
                        window.get_height() // 2 - label.get_height() // 2))
    pygame.display.flip()
def loading(window):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obsługa klawiszy
        keys = pygame.key.get_pressed()
        drawLoadingScreen(window)

    # Zamykanie Pygame
    pygame.quit()
    sys.exit()


