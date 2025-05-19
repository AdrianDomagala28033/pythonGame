import pygame

from gameCode.Classes.levels.levelElements.door import Door
from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.levels.game import game

pygame.init()
clock = pygame.time.Clock()

# --- funkcja do ładowania klatek z sprite sheeta ---
def load_fire_frames(sprite_sheet_path, frame_width, frame_height, frame_count, scale_to=(1280, 128)):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    frames = []

    for i in range(frame_count):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surface.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(frame_surface, scale_to)
        frames.append(scaled_frame)

    return frames


pygame.init()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dungeon Escape - Test")
clock = pygame.time.Clock()

# Załaduj poziom


def menu(window):
    run = True
    button = pygame.image.load("./images/playButton.PNG").convert_alpha()
    button_rect = button.get_rect(center=(620, 400))
    gameName = pygame.image.load("./images/gameName.PNG").convert_alpha()
    fire_frames = load_fire_frames("./images/fireAnimation.png", 214, 500, 6, scale_to=(180, 500))
    current_frame = 0
    frame_timer = 0
    frame_speed = 5
    frame_direction = 1
    level = Level([], [], [], [], [], Door(0,0), [],0, 0)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if button_rect.collidepoint(event.pos):
                game(window)
                run = False
        frame_timer += 1
        if frame_timer >= frame_speed:
            current_frame += frame_direction

            if current_frame == len(fire_frames) - 1 or current_frame == 0:
                frame_direction *= -1  # zmień kierunekLevel

            frame_timer = 0
        window.fill((20, 20, 20))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 12), f"Alpha 1.0", True, (255, 255, 255)),
                    (1230, 0))
        window.blit(gameName, (500, 0))
        for x in range(0, 1280, 180):
            window.blit(fire_frames[current_frame], (x, 400))
        window.blit(button, button_rect)

        pygame.display.update()
