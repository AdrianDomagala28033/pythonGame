import random
roomTypes = [
'start', # punkt startowy gracza
'enemy', # zwykły pokój z wrogami
'key', # zawiera klucz (potrzebny do wyjścia)
'exit', # wyjście z poziomu
'loot', # skarby, monety, skrzynki
'quest', # NPC z zadaniem
'shop', # sklep z bronią/itemami
'boss', # większy pokój z trudnym wrogiem
'secret' # opcjonalny, niepołączony z główną ścieżką
]

def generateRoom(roomType, exits):
    width = random.choice([22, 24, 26, 28])
    height = random.choice([12, 14, 16])

    layout = [['#' for _ in range(width)] for _ in range(height)]

    # Wypełnij środek powietrzem
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            layout[y][x] = '.'

    centerX = width // 2
    centerY = height // 2

    # Zakazane strefy dla platform (np. wejścia/wyjścia)
    blockedZones = set()

    if 'left' in exits:
        for dy in [-1, 0, 1]:
            layout[centerY + dy][0] = '.'
            layout[centerY + dy][1] = '.'

    if 'right' in exits:
        for dy in [-1, 0, 1]:
            layout[centerY + dy][-1] = '.'
            layout[centerY + dy][-2] = '.'

    if 'top' in exits:
        for dx in [-1, 0, 1]:
            layout[0][centerX + dx] = '.'
            layout[1][centerX + dx] = '.'

    if 'bottom' in exits:
        for dx in [-1, 0, 1]:
            layout[-1][centerX + dx] = '.'
            layout[-2][centerX + dx] = '.'

    # Dodaj platformy
    for _ in range(10):
        platY = random.randint(3, height - 4)
        platX = random.randint(2, width - 7)

        canPlace = True
        for dx in range(5):
            for dy in [-2, -1, 0, 1]:
                px = platX + dx
                py = platY + dy
                if not (0 <= px < width and 0 <= py < height):
                    canPlace = False
                if (px, py) in blockedZones:
                    canPlace = False
                if layout[py][px] != '.':
                    canPlace = False

        if canPlace:
            for dx in range(5):
                layout[platY][platX + dx] = '#'

    # Obiekty specjalne
    if roomType == 'start':
        layout[centerY][2] = 'P'

    elif roomType == 'exit':
        layout[centerY][-3] = 'D'

    elif roomType == 'key':
        layout[centerY][centerX] = 'K'

    elif roomType == 'loot':
        layout[centerY][centerX] = 'c'
        layout[centerY + 1][centerX - 2] = 'C'
        layout[centerY + 1][centerX + 2] = 'C'

    elif roomType == 'shop':
        layout[centerY][centerX] = 'Q'  # NPC/sklep
        layout[centerY][centerX - 2] = 'c'
        layout[centerY][centerX + 2] = 'C'

    elif roomType == 'quest':
        layout[centerY][centerX] = 'Q'

    elif roomType == 'boss':
        layout[centerY][centerX] = 'R'
        layout[centerY - 1][centerX - 2] = 'E'
        layout[centerY - 1][centerX + 2] = 'E'

    elif roomType == 'secret':
        layout[centerY][centerX] = 'c'
        layout[centerY + 1][centerX] = 'C'

    # Przejścia 2x2
    if 'left' in exits:
        layout[centerY - 1][0] = '.'
        layout[centerY][0] = '.'
        layout[centerY - 1][1] = '.'
        layout[centerY][1] = '.'

    if 'right' in exits:
        layout[centerY - 1][-1] = '.'
        layout[centerY][-1] = '.'
        layout[centerY - 1][-2] = '.'
        layout[centerY][-2] = '.'

    if 'top' in exits:
        layout[0][centerX - 1] = '.'
        layout[0][centerX] = '.'
        layout[1][centerX - 1] = '.'
        layout[1][centerX] = '.'
        # platforma pod wejściem
        for dx in range(-2, 3):
            layout[3][centerX + dx] = '#'

    if 'bottom' in exits:
        layout[-1][centerX - 1] = '.'
        layout[-1][centerX] = '.'
        layout[-2][centerX - 1] = '.'
        layout[-2][centerX] = '.'
        # platforma nad wyjściem
        for dx in range(-2, 3):
            layout[height - 4][centerX + dx] = '#'

    if random.random() < 0.3:
        tx = random.randint(3, width - 5)
        for dy in range(3, height - 3):
            layout[dy][tx] = '.'
            if random.random() < 0.5:
                layout[dy][tx + 1] = '.'

    for _ in range(random.randint(1, 3)):
        platY = random.randint(3, height - 4)
        platX = random.randint(2, width - 7)
        if all(layout[platY][platX + dx] == '.' for dx in range(5)):
            for dx in range(5):
                layout[platY][platX + dx] = '#'

    return [''.join(row) for row in layout], width, height

