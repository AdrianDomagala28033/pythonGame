import pygame
from gameCode.levels.menu import menu


pygame.init()
window = pygame.display.set_mode((1280, 700))

if __name__ == "__main__":
    menu(window)

