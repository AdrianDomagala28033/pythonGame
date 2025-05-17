from perlin_noise import PerlinNoise
import random

TILE_SIZE = 50
LEVEL_WIDTH = 100
LEVEL_HEIGHT = 30
PLAYER_HEIGHT = 2
PLAYER_JUMP_HEIGHT = 4
ROOM_COUNT = 4
ROOM_WIDTH = LEVEL_WIDTH // ROOM_COUNT

def generate_normal_level():
    SEED = random.randint(0, 10000)
    noise = PerlinNoise(octaves=3, seed=SEED)
    level = [['#' for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]

    # Utwórz główny tunel przez kilka "pokoi"
    pathY = []
    currentY = LEVEL_HEIGHT // 2

    for r in range(ROOM_COUNT):
        roomStart = r * ROOM_WIDTH
        roomEnd = (r + 1) * ROOM_WIDTH

        # Losowa wysokość wejścia i wyjścia z pokoju
        roomY = max(2, min(LEVEL_HEIGHT - PLAYER_HEIGHT - 2, currentY + random.choice([-1, 0, 1])))
        currentY = roomY

        for x in range(roomStart, roomEnd):
            y = roomY
            pathY.append(y)
            for h in range(-PLAYER_JUMP_HEIGHT, PLAYER_HEIGHT + 1):
                newY = y + h
                if 0 <= newY < LEVEL_HEIGHT:
                    level[newY][x] = '.'

        # Dodaj "komnatę" (rozszerzenie przestrzeni) w środku pokoju
        for _ in range(random.randint(3, 5)):
            rx = random.randint(roomStart + 2, roomEnd - 3)
            ry = random.randint(currentY - 2, currentY + 2)
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx = rx + dx
                    ny = ry + dy
                    if 0 < nx < LEVEL_WIDTH - 1 and 0 < ny < LEVEL_HEIGHT - 1:
                        level[ny][nx] = '.'

    # Dodaj lekkie wygładzenie perlinowe (opcjonalne)
    threshold = 0.2
    for y in range(1, LEVEL_HEIGHT - 1):
        for x in range(1, LEVEL_WIDTH - 1):
            n = noise([x / LEVEL_WIDTH, y / LEVEL_HEIGHT])
            if n > threshold:
                level[y][x] = '.'

    # Dodaj gracza i drzwi na końcach tunelu
    startX = 1
    endX = LEVEL_WIDTH - 2
    level[pathY[startX]][startX] = 'P'
    level[pathY[endX]][endX] = 'D'

    # Dodaj ramkę wokół mapy
    for x in range(LEVEL_WIDTH):
        level[0][x] = '#'
        level[LEVEL_HEIGHT - 1][x] = '#'
    for y in range(LEVEL_HEIGHT):
        level[y][0] = '#'
        level[y][LEVEL_WIDTH - 1] = '#'

    return level
def generate_single_cave_level():
    SEED = random.randint(0, 10000)
    noise = PerlinNoise(octaves=4, seed=SEED)
    threshold = 0.1

    # Start: plansza z ramką
    level = [['#' for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]

    # Wyznacz główny tunel
    pathY = [LEVEL_HEIGHT // 2]
    for x in range(1, LEVEL_WIDTH - 1):
        lastY = pathY[-1]
        delta = random.choice([-1, 0, 1])
        newY = max(2, min(LEVEL_HEIGHT - PLAYER_HEIGHT - 2, lastY + delta))
        pathY.append(newY)

    # Otwórz korytarz
    for x in range(1, LEVEL_WIDTH - 1):
        y = pathY[x - 1]
        for h in range(-PLAYER_JUMP_HEIGHT, PLAYER_HEIGHT + 1):
            ny = y + h
            if 1 <= ny < LEVEL_HEIGHT - 1:
                level[ny][x] = '.'

    # Dodaj pokoje losowo przy tunelu
    for x in range(10, LEVEL_WIDTH - 10, 10):
        y = pathY[x]
        room_width = random.randint(4, 6)
        room_height = random.randint(3, 5)
        for dx in range(-room_width // 2, room_width // 2 + 1):
            for dy in range(-room_height // 2, room_height // 2 + 1):
                rx, ry = x + dx, y + dy
                if 1 <= ry < LEVEL_HEIGHT - 1 and 1 <= rx < LEVEL_WIDTH - 1:
                    level[ry][rx] = '.'

    # Dodatkowe wygładzenie (opcjonalne)
    for y in range(1, LEVEL_HEIGHT - 1):
        for x in range(1, LEVEL_WIDTH - 1):
            n = noise([x / LEVEL_WIDTH, y / LEVEL_HEIGHT])
            if n > threshold and level[y][x] == '#':
                level[y][x] = '.'

    # Dodaj gracza
    playerX = 1
    playerY = pathY[playerX]
    level[playerY][playerX] = 'P'

    # Dodaj drzwi
    doorX = LEVEL_WIDTH - 2
    doorY = pathY[doorX]
    level[doorY][doorX] = 'D'

    return level
def generate_cave_with_floors():
    LEVEL_WIDTH = random.randint(90, 130)
    FLOORS = random.randint(2, 4)
    FLOOR_GAP = random.randint(9, 13)
    FLOOR_HEIGHT = random.randint(6, 10)

    LEVEL_HEIGHT = FLOORS * FLOOR_GAP + 4
    PLAYER_HEIGHT = 2
    PLAYER_JUMP_HEIGHT = 4

    noise = PerlinNoise(octaves=4, seed=random.randint(0, 10000))

    level = [['#' for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]

    floorYs = [2 + i * FLOOR_GAP for i in range(FLOORS)]

    # Kilka losowych przejść między piętrami
    stairXs = sorted(random.sample(range(10, LEVEL_WIDTH - 10), k=random.randint(FLOORS, FLOORS + 2)))

    for i, baseY in enumerate(floorYs):
        # Tworzenie głównej ścieżki tunelu
        pathY = [baseY + FLOOR_HEIGHT // 2]
        for x in range(1, LEVEL_WIDTH - 1):
            lastY = pathY[-1]
            delta = random.choice([-1, 0, 1])
            newY = max(baseY, min(baseY + FLOOR_HEIGHT - PLAYER_HEIGHT, lastY + delta))
            pathY.append(newY)

        # Wyżłobienie tunelu
        for x in range(1, LEVEL_WIDTH - 1):
            y = pathY[x - 1]
            tunnelHeight = random.randint(PLAYER_HEIGHT, PLAYER_HEIGHT + 2)
            for h in range(-PLAYER_JUMP_HEIGHT, tunnelHeight + 1):
                ny = y + h
                if 1 <= ny < LEVEL_HEIGHT - 1:
                    level[ny][x] = '.'

        # Dodanie pokojów
        for x in range(10, LEVEL_WIDTH - 10, random.randint(10, 15)):
            y = pathY[x]
            room_width = random.randint(4, 8)
            room_height = random.randint(3, 5)
            for dx in range(-room_width // 2, room_width // 2 + 1):
                for dy in range(-room_height // 2, room_height // 2 + 1):
                    rx, ry = x + dx, y + dy
                    if 1 <= ry < LEVEL_HEIGHT - 1 and 1 <= rx < LEVEL_WIDTH - 1:
                        level[ry][rx] = '.'

        # Przejścia pionowe z aktualnego piętra do niższego
        if i < FLOORS - 1:
            stairsThisFloor = random.sample(stairXs, k=min(len(stairXs), 2))
            for x in stairsThisFloor:
                for y in range(baseY + FLOOR_HEIGHT, baseY + FLOOR_GAP):
                    if 1 <= y < LEVEL_HEIGHT - 1:
                        level[y][x] = 'G'
        platformCount = random.randint(10, 18)  # więcej platform!
        for _ in range(platformCount):
            platLength = random.randint(3, 7)  # dłuższe platformy
            platX = random.randint(2, LEVEL_WIDTH - platLength - 2)
            platY = random.randint(baseY + 1, baseY + FLOOR_HEIGHT - 1)

            # Upewnij się, że platforma nie koliduje z podłogą tunelu
            isSafe = all(level[platY][platX + dx] == '.' for dx in range(platLength))
            if isSafe:
                for dx in range(platLength):
                    level[platY][platX + dx] = '#'


    # Dodaj gracza (start górne piętro)
    playerX = 2
    playerY = floorYs[0] + FLOOR_HEIGHT // 2
    level[playerY][playerX] = 'P'

    # Dodaj drzwi (koniec na dolnym piętrze)
    doorX = LEVEL_WIDTH - 3
    doorY = floorYs[-1] + FLOOR_HEIGHT // 2
    level[doorY][doorX] = 'D'
    keyX = random.randint(5, LEVEL_WIDTH - 15)
    keyY = random.randint(5, LEVEL_HEIGHT - 15)
    print(f"Kordy klucza x:{keyX} y:{keyY}")
    if level[keyY][keyX] == ".":
        level[keyY][keyX] = "K"


    # Ramka poziomu
    for x in range(LEVEL_WIDTH):
        level[0][x] = '#'
        level[-1][x] = '#'
    for y in range(LEVEL_HEIGHT):
        level[y][0] = '#'
        level[y][-1] = '#'

    return level