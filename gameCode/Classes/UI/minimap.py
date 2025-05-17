import pygame


def drawMiniMap(window, levelData, player, tileSize=4, topRight=(1280, 0)):
    TILE_SIZE = 50  # zakładamy kafelek 32x32

    mapWidth = len(levelData[0])
    topLeftX = topRight[0] - mapWidth * tileSize
    topLeftY = topRight[1]

    for y, row in enumerate(levelData):
        for x, cell in enumerate(row):
            color = (0, 0, 0)
            if cell == "#":
                color = (50, 50, 50)
            elif cell == ".":
                color = (150, 150, 150)
            elif cell == "D":
                color = (255, 255, 0)
            elif cell == "K":
                color = (255, 255, 255)
            elif cell == "C":
                color = (255, 215, 0)
            elif cell in ("E", "R"):
                color = (255, 0, 0)
            elif cell in ("T", "B"):
                color = (100, 80, 40)

            rect = pygame.Rect(topLeftX + x * tileSize,
                               topLeftY + y * tileSize,
                               tileSize, tileSize)
            pygame.draw.rect(window, color, rect)

    # Uwzględnij scroll kamery
    globalX, globalY = player.hitbox.center

    gridX = int(globalX // TILE_SIZE)
    gridY = int(globalY // TILE_SIZE)

    if 0 <= gridY < len(levelData) and 0 <= gridX < len(levelData[0]):
        px = topLeftX + gridX * tileSize
        py = topLeftY + gridY * tileSize
        pygame.draw.rect(window, (0, 255, 0), (px, py, tileSize, tileSize))