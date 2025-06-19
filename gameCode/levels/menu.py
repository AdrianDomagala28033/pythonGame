from gameCode.visualEffects.FogParticle import create_fog_texture_with_cache, generate_dungeon_wall_texture
from gameCode.levels.game import game

import pygame
import sys

pygame.init()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dungeon Escape")
clock = pygame.time.Clock()

def menu(window):
    run = True
    t = 0.0
    # Mgła – generowana raz
    fog_texture = create_fog_texture_with_cache(1600, 900, filename="staticFog.png", scale=100, octaves=4)
    fog_scroll_x = 0
    fog_scroll_y = 0
    # 🔥 Animacja tła
    wall_texture = generate_dungeon_wall_texture(512, window_height)


    # Fonty
    title_font = pygame.font.Font("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 72)
    button_font = pygame.font.Font("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 36)
    small_font = pygame.font.SysFont("arial", 14)

    title_text = title_font.render("Dungeon Escape", True, (255, 255, 255))
    version_text = small_font.render("Alpha 1.0", True, (255, 255, 255))

    # Przyciski
    buttons = [
        {"label": "▶ Nowa gra", "action": "start"},
        {"label": "⏯ Kontynuuj", "action": "continue"},
        {"label": "⚙ Opcje", "action": "options"},
    ]
    button_rects = []

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        action = buttons[i]["action"]
                        if action == "start":
                            pygame.mixer.music.stop()
                            game(window)
                            run = False
                        elif action == "continue":
                            print("⏯ Kontynuuj – TODO: wczytaj zapis gry")
                        elif action == "options":
                            print("⚙ Opcje – TODO: otwórz ustawienia")

        # Aktualizacja mgły
        fog_scroll_x = (fog_scroll_x + 0.3) % fog_texture.get_width()
        fog_scroll_y = (fog_scroll_y + 0.1) % fog_texture.get_height()

        # Tworzymy animowany ogień o szerokości całego ekranu i wysokości fire_height


        # Rysuj tło

        window.fill((15, 15, 15))

        # Rysuj przewijaną mgłę (tile)
        bg_scroll_x = int(t * 30) % wall_texture.get_width()
        for x in range(-wall_texture.get_width(), window_width + wall_texture.get_width(), wall_texture.get_width()):
            window.blit(wall_texture, (x - bg_scroll_x, 0))

        # Nałóż animowaną poświatę/światło

        for x in range(-fog_texture.get_width(), window_width + fog_texture.get_width(), fog_texture.get_width()):
            for y in range(-fog_texture.get_height(), window_height + fog_texture.get_height(),
                           fog_texture.get_height()):
                window.blit(fog_texture, (x - fog_scroll_x, y - fog_scroll_y))


        # Tytuł
        window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 100))

        # Przyciski
        mouse_pos = pygame.mouse.get_pos()
        button_rects = []
        start_y = 340
        spacing = 70
        for i, btn in enumerate(buttons):
            label = btn["label"]
            text_surface = button_font.render(label, True, (255, 255, 255))
            width = text_surface.get_width() + 40
            height = text_surface.get_height() + 20
            rect = pygame.Rect((window_width // 2 - width // 2, start_y + i * spacing), (width, height))
            is_hovered = rect.collidepoint(mouse_pos)

            bg_color = (40, 40, 40) if not is_hovered else (60, 80, 60)
            border_color = (255, 255, 255)
            pygame.draw.rect(window, bg_color, rect, border_radius=8)
            pygame.draw.rect(window, border_color, rect, 2, border_radius=8)
            window.blit(text_surface, (rect.centerx - text_surface.get_width() // 2,
                                       rect.centery - text_surface.get_height() // 2))

            button_rects.append(rect)

        # Wersja
        window.blit(version_text, (window_width - 80, 10))

        pygame.display.update()


