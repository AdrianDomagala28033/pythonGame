from cProfile import label

import pygame


def drawPanelBackground(surface, width, height, alpha=220):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0,0,0, alpha))
    pygame.draw.rect(overlay, (255, 255, 255), overlay.get_rect(), 2)
    return overlay
def drawHighlightedText(surface, rect, text, font, selected=False, color=(255,255,255)):
    bgColor = (80,80,80) if selected else (30,30,30)
    pygame.draw.rect(surface, bgColor, rect)
    pygame.draw.rect(surface,(255,255,255), rect, 1)
    label = font.render(text, True, color)
    surface.blit(label, (rect.x + 10, rect.y + 5))

def getHoverIndex(buttons, mousePos):
    for i, (_, rect) in enumerate(buttons):
        if rect.collidepoint(mousePos):
            return i
    return None