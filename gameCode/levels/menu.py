import pygame
from gameCode.levels.levelOne import levelOne

pygame.init()
clock = pygame.time.Clock()

# --- funkcja do ładowania klatek z sprite sheeta ---
def load_fire_frames(sprite_sheet_path, frame_width, frame_height, frame_count):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    frames = []

    for i in range(frame_count):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surface.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
        frames.append(frame_surface)

    return frames


def menu(window):
    run = True
    button = pygame.image.load("./images/playButton.PNG").convert_alpha()
    button_rect = button.get_rect(center=(620, 400))
    gameName = pygame.image.load("./images/gameName.PNG").convert_alpha()
    fire_frames = load_fire_frames("./images/fireAnimation.png", 1280, 128, 6)
    current_frame = 0
    frame_timer = 0
    frame_speed = 5
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if button_rect.collidepoint(event.pos):
                levelOne(window)
                run = False
        frame_timer += 1
        if frame_timer >= frame_speed:
            current_frame = (current_frame + 1) % len(fire_frames)
            frame_timer = 0
        window.fill((20, 20, 20))
        window.blit(gameName, (500, 0))
        window.blit(button, button_rect)
        for i, frame in enumerate(fire_frames):
            window.blit(frame, (0, 620 + i * 130))
        pygame.display.update()
