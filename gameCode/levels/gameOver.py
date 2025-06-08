import pygame

def back_to_menu(window):
    from gameCode.levels.menu import menu
    menu(window)


def gameOver(window):
    run = True
    clock = 0
    button = pygame.image.load("./images/playButton.PNG").convert_alpha()
    button_rect = button.get_rect(center=(620, 400))
    while run:
        clock = pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if button_rect.collidepoint(event.pos):
                    back_to_menu(window)
                    run = False

        window.fill((0, 4, 0))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Game Over", True, (255, 255, 255)),(500, 0))
        window.blit(button, button_rect)
        pygame.display.update()