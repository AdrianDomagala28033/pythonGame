import random

from perlin_noise import PerlinNoise

from gameCode.Classes.levels.levelManagment.generator.newGenerator.levelBuilder import stitchRooms, stitchRoomsDynamic, \
    stitchRoomsNatural

from gameCode.Classes.levels.levelManagment.generator.newGenerator.roomMap import generateRoomMap


def generateLevel():
    roomMap = generateRoomMap(5, 5)
    return stitchRoomsDynamic(roomMap)

def generateOpenLevel(width=160, height=60):
    PLAYER_HEIGHT = 2
    PLAYER_JUMP_HEIGHT = 4
    noise = PerlinNoise(octaves=4, seed=random.randint(0, 10000))
    level = [['#' for _ in range(width)] for _ in range(height)]

    # 1. Główna ścieżka przez mapę
    pathY = [height // 2]
    for x in range(1, width):
        lastY = pathY[-1]
        delta = random.choice([-1, 0, 1])
        newY = max(3, min(height - PLAYER_HEIGHT - 3, lastY + delta))
        pathY.append(newY)

    for x in range(width):
        y = pathY[x]
        for dy in range(-PLAYER_JUMP_HEIGHT, PLAYER_HEIGHT + 2):
            ny = y + dy
            if 1 <= ny < height - 1:
                level[ny][x] = '.'

    # 2. Dodaj pokoje typu „komory” wzdłuż ścieżki
    for x in range(10, width - 10, 12):
        y = pathY[x]
        for dx in range(-4, 5):
            for dy in range(-3, 4):
                nx, ny = x + dx, y + dy
                if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                    level[ny][nx] = '.'

    # 3. Dodaj platformy losowo
    for _ in range(60):
        x = random.randint(4, width - 8)
        y = random.randint(6, height - 6)

        # Sprawdź czy miejsce jest wystarczająco otwarte
        if all(level[y][x + dx] == '.' for dx in range(5)) and \
                all(level[y - 1][x + dx] == '.' for dx in range(5)) and \
                all(level[y + 1][x + dx] == '.' for dx in range(5)):
            for dx in range(5):
                level[y][x + dx] = '#'

    # 4. Dodaj gracza i drzwi
    level[pathY[1]][1] = 'P'
    level[pathY[-2]][width - 2] = 'D'

    # 5. Dodaj klucz
    for _ in range(20):
        x = random.randint(10, width - 10)
        y = pathY[x]
        if level[y][x] == '.':
            level[y][x] = 'K'
            break

    # 6. Dodaj przeciwników, skrzynki, monety
    enemies = ['E', 'R']
    maxEnemies = width // 4
    maxCoins = width // 3
    maxChests = width // 12

    def placeRandom(char, conditionFn):
        count = 0
        for _ in range(200):
            if count >= char[1]:
                break
            x = random.randint(2, width - 3)
            y = random.randint(2, height - 3)
            if conditionFn(x, y):
                level[y][x] = char[0]
                count += 1

    placeRandom(('E', maxEnemies), lambda x, y: level[y + 1][x] == '#' and level[y][x] == '.')
    placeRandom(('R', maxEnemies // 2), lambda x, y: level[y + 1][x] == '#' and level[y][x] == '.')
    placeRandom(('C', maxCoins), lambda x, y: level[y][x] == '.' and level[y][x] not in ['P', 'D', 'K', 'E', 'R'])
    placeRandom(('c', maxChests), lambda x, y: level[y + 1][x] == '#' and level[y][x] == '.')

    # Ramka
    for x in range(width):
        level[0][x] = '#'
        level[height - 1][x] = '#'
    for y in range(height):
        level[y][0] = '#'
        level[y][width - 1] = '#'

    return [''.join(row) for row in level]

def generateDeadCellsStyleLevel(width=160, height=60):
    PLAYER_HEIGHT = 2
    PLAYER_JUMP_HEIGHT = 4
    level = [['#' for _ in range(width)] for _ in range(height)]
    noise = PerlinNoise(octaves=3, seed=random.randint(0, 10000))
    # 1. Główna ścieżka
    pathY = [height // 2]
    for x in range(1, width):
        delta = round(noise([x / width]) * 2)
        newY = max(4, min(height - 5, pathY[-1] + delta))
        pathY.append(newY)

    # 2. Wydrąż tunel
    for x in range(width):
        y = pathY[x]
        for dy in range(-PLAYER_JUMP_HEIGHT - 1, PLAYER_HEIGHT + 2):
            ny = y + dy
            if 1 <= ny < height - 1:
                level[ny][x] = '.'

    # 3. Dodaj otwarte pokoje nad i pod trasą
    for x in range(10, width - 10, 12):
        y = pathY[x]

        if random.random() < 0.5:
            # Pokój nad
            roomW = random.randint(6, 10)
            roomH = random.randint(4, 6)
            ox = x - roomW // 2
            oy = y - PLAYER_JUMP_HEIGHT - 3 - roomH
        else:
            # Pokój pod
            roomW = random.randint(6, 10)
            roomH = random.randint(4, 6)
            ox = x - roomW // 2
            oy = y + PLAYER_HEIGHT + 3

        for dx in range(roomW):
            for dy in range(roomH):
                tx = ox + dx
                ty = oy + dy
                if 1 <= tx < width - 1 and 1 <= ty < height - 1:
                    level[ty][tx] = '.'

    # 4. Dodaj platformy (górne, boczne piętra)
    for _ in range(50):
        platW = random.randint(4, 6)
        x = random.randint(3, width - platW - 3)
        y = random.randint(5, height - 6)
        if all(level[y][x + dx] == '.' for dx in range(platW)) and \
                all(level[y + 1][x + dx] == '.' for dx in range(platW)):
            for dx in range(platW):
                level[y][x + dx] = '#'

    # 5. Gracz, drzwi, klucz
    level[pathY[1]][1] = 'P'
    level[pathY[-2]][width - 2] = 'D'

    for _ in range(30):
        x = random.randint(10, width - 10)
        y = pathY[x]
        if level[y][x] == '.':
            level[y][x] = 'K'
            break

    # 6. Przeciwnicy, loot
    def place(char, count, cond):
        placed = 0
        for _ in range(500):
            if placed >= count: break
            x = random.randint(2, width - 3)
            y = random.randint(2, height - 3)
            if cond(x, y):
                level[y][x] = char
                placed += 1

    place('E', width // 4, lambda x, y: level[y][x] == '.' and level[y + 1][x] == '#')
    place('R', width // 8, lambda x, y: level[y][x] == '.' and level[y + 1][x] == '#')
    place('C', width // 3, lambda x, y: level[y][x] == '.' and level[y][x] not in ['P', 'D', 'K', 'E', 'R'])
    place('c', width // 15, lambda x, y: level[y][x] == '.' and level[y + 1][x] == '#')

    # 7. Ramka
    for x in range(width):
        level[0][x] = level[height - 1][x] = '#'
    for y in range(height):
        level[y][0] = level[y][-1] = '#'

    return [''.join(row) for row in level]

def generateNaturalModularLevel():
    roomMap = generateRoomMap(5, 4)
    return stitchRoomsNatural(roomMap)