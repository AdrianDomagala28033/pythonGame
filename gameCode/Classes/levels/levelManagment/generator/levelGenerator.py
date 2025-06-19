from networkx.algorithms.bipartite.generators import random_graph
from perlin_noise import PerlinNoise
import random
from gameCode.Classes.levels.levelManagment.generator.room import Room
from gameCode.Classes.levels.levelManagment.generator.roomTemplates import roomTemplates
from gameCode.Classes.levels.levelManagment.levelLoading import load_from_text_lines

TILE_SIZE = 50
LEVEL_WIDTH = random.randint(100, 175)
LEVEL_HEIGHT = random.randint(30,60)
PLAYER_HEIGHT = 2
PLAYER_JUMP_HEIGHT = 4
ROOM_COUNT = 4
ROOM_WIDTH = LEVEL_WIDTH // ROOM_COUNT
def generate_cave_with_floors():
    LEVEL_WIDTH = random.randint(90, 130)
    FLOORS = random.randint(2, 4)
    FLOOR_GAP = random.randint(9, 13)
    FLOOR_HEIGHT = random.randint(5, 8)

    LEVEL_HEIGHT = FLOORS * FLOOR_GAP + 4
    PLAYER_HEIGHT = 2
    PLAYER_JUMP_HEIGHT = 4

    noise = PerlinNoise(octaves=4, seed=random.randint(0, 10000))

    level = [['#' for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]

    floorYs = [2 + i * FLOOR_GAP for i in range(FLOORS)]

    stairXs = sorted(random.sample(range(10, LEVEL_WIDTH - 10), k=random.randint(FLOORS, FLOORS + 2)))

    for i, baseY in enumerate(floorYs):
        pathY = [baseY + FLOOR_HEIGHT // 2]
        for x in range(1, LEVEL_WIDTH - 1):
            lastY = pathY[-1]
            delta = random.choice([-1, 0, 1])
            newY = max(baseY, min(baseY + FLOOR_HEIGHT - PLAYER_HEIGHT, lastY + delta))
            pathY.append(newY)

        for x in range(1, LEVEL_WIDTH - 1):
            y = pathY[x - 1]
            tunnelHeight = random.randint(PLAYER_HEIGHT, PLAYER_HEIGHT + 2)
            for h in range(-PLAYER_JUMP_HEIGHT, tunnelHeight + 1):
                ny = y + h
                if 1 <= ny < LEVEL_HEIGHT - 1:
                    level[ny][x] = '.'

        for x in range(10, LEVEL_WIDTH - 10, random.randint(10, 15)):
            y = pathY[x]
            room_width = random.randint(4, 8)
            room_height = random.randint(3, 5)
            for dx in range(-room_width // 2, room_width // 2 + 1):
                for dy in range(-room_height // 2, room_height // 2 + 1):
                    rx, ry = x + dx, y + dy
                    if 1 <= ry < LEVEL_HEIGHT - 1 and 1 <= rx < LEVEL_WIDTH - 1:
                        level[ry][rx] = '.'

        if i < FLOORS - 1:
            stairsThisFloor = random.sample(stairXs, k=min(len(stairXs), 2))
            for x in stairsThisFloor:
                hole_height = FLOOR_GAP - FLOOR_HEIGHT
                hole_width = 6
                hole_y_start = baseY + FLOOR_HEIGHT
                for dx in range(-hole_width // 2, hole_width // 2 + 1):
                    for dy in range(hole_height):
                        ny = hole_y_start + dy
                        nx = x + dx
                        if 1 <= ny < LEVEL_HEIGHT - 1 and 1 <= nx < LEVEL_WIDTH - 1:
                            level[ny][nx] = '.'

    for i in range(FLOORS - 1):
        baseY = floorYs[i]
        nextBaseY = floorYs[i + 1]
        vertical_space = nextBaseY - baseY - FLOOR_HEIGHT

        platform_count = max(3, vertical_space // 2)

        for p in range(platform_count):
            plat_y = baseY + FLOOR_HEIGHT + 2 + p * 2

            possible_xs = []
            for x in range(2, LEVEL_WIDTH - 6):
                above_clear = all(level[plat_y - 1 - dy][x + dx] == '.' for dx in range(4) for dy in range(2))
                below_clear = all(level[plat_y + 1 + dy][x + dx] == '.' for dx in range(4) for dy in range(2))
                place_clear = all(level[plat_y][x + dx] == '.' for dx in range(4))
                if above_clear and below_clear and place_clear:
                    possible_xs.append(x)

            if possible_xs:
                plat_x = random.choice(possible_xs)
                for dx in range(4):
                    level[plat_y][plat_x + dx] = '#'

    playerX = 2
    playerY = floorYs[0] + FLOOR_HEIGHT // 2
    level[playerY][playerX] = 'P'

    doorX = LEVEL_WIDTH - 3
    doorY = floorYs[-1] + FLOOR_HEIGHT // 2
    level[doorY][doorX] = 'D'
    keyX = random.randint(5, LEVEL_WIDTH - 15)
    keyY = random.randint(5, LEVEL_HEIGHT - 15)
    if level[keyY][keyX] == ".":
        level[keyY][keyX] = "K"
    for x in range(LEVEL_WIDTH):
        level[0][x] = '#'
        level[-1][x] = '#'
    for y in range(LEVEL_HEIGHT):
        level[y][0] = '#'
        level[y][-1] = '#'

    # --- Dodanie przeciwników i monet ---
    enemy_types = ['E', 'R']
    max_enemies = LEVEL_WIDTH * FLOORS // 10  # liczba przeciwników zależna od rozmiaru
    max_coins = LEVEL_WIDTH * FLOORS // 8  # liczba monet
    max_chests =  LEVEL_WIDTH * FLOORS // 30

    enemies_placed = 0
    coins_placed = 0
    chestPlaced = 0

    # Rozmieszczanie przeciwników na podłożu/platformach
    while enemies_placed < max_enemies:
        x = random.randint(2, LEVEL_WIDTH - 3)
        y = random.randint(2, LEVEL_HEIGHT - 3)

        # Na podłożu/platformie (#) i powyżej powietrze (.)
        if (level[y][x] == '#'
                and level[y - 1][x] == '.'
                and level[y][x] != 'P' and level[y][x] != 'D'):
            # Sprawdź, czy miejsce wolne od innych wrogów
            if all(level[y - 1][xx] != 'E' and level[y - 1][xx] != 'R' for xx in
                   range(max(0, x - 1), min(LEVEL_WIDTH, x + 2))):
                enemy_char = random.choice(enemy_types)
                level[y - 1][x] = enemy_char
                enemies_placed += 1

    # Rozmieszczanie monet na powietrzu
    while coins_placed < max_coins:
        x = random.randint(2, LEVEL_WIDTH - 3)
        y = random.randint(2, LEVEL_HEIGHT - 3)
        if (level[y][x] == '.'
                and level[y][x] != 'P' and level[y][x] != 'D'):
            level[y][x] = 'C'
            coins_placed += 1
    while chestPlaced < max_chests:
        x = random.randint(2, LEVEL_WIDTH - 3)
        y = random.randint(2, LEVEL_HEIGHT - 3)
        if (level[y][x] == '.'
                and level[y][x] != 'P' and level[y][x] != 'D' and level[y][x] != 'C' and level[y+1][x] == "#"):
            level[y][x] = 'c'
            chestPlaced += 1

    return level
def generate_single_cave_level():
    SEED = random.randint(0, 10000)
    noise = PerlinNoise(octaves=4, seed=SEED)
    threshold = 0.01

    level = [['#' for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]

    pathY = [LEVEL_HEIGHT // 2]
    for x in range(1, LEVEL_WIDTH - 1):
        lastY = pathY[-1]
        delta = random.choice([-1, 0, 1])
        newY = max(2, min(LEVEL_HEIGHT - PLAYER_HEIGHT - 2, lastY + delta))
        pathY.append(newY)

    for x in range(1, LEVEL_WIDTH - 1):
        y = pathY[x - 1]
        for h in range(-PLAYER_JUMP_HEIGHT, PLAYER_HEIGHT + 1):
            ny = y + h
            if 1 <= ny < LEVEL_HEIGHT - 1:
                level[ny][x] = '.'

    room_centers = []
    for x in range(10, LEVEL_WIDTH - 10, 10):
        y = pathY[x]
        room_width = random.randint(4, 6)
        room_height = random.randint(3, 5)
        for dx in range(-room_width // 2, room_width // 2 + 1):
            for dy in range(-room_height // 2, room_height // 2 + 1):
                rx, ry = x + dx, y + dy
                if 1 <= ry < LEVEL_HEIGHT - 1 and 1 <= rx < LEVEL_WIDTH - 1:
                    level[ry][rx] = '.'
        room_centers.append((x, y))

    for y in range(1, LEVEL_HEIGHT - 1):
        for x in range(1, LEVEL_WIDTH - 1):
            n = noise([x / LEVEL_WIDTH, y / LEVEL_HEIGHT])
            if n > threshold and level[y][x] == '#':
                level[y][x] = '.'

    playerX = 1
    playerY = pathY[playerX]
    level[playerY][playerX] = 'P'

    doorX = LEVEL_WIDTH - 2
    doorY = pathY[doorX]
    level[doorY][doorX] = 'D'

    # Klucz
    keyX = random.randint(5, 15)
    keyY = pathY[keyX]
    level[keyY][keyX] = 'K'

    # Platformy: więcej, dłuższe, niżej
    for y in range(4, LEVEL_HEIGHT - 4):  # zostaw marginesy góra/dół
        for x in range(3, LEVEL_WIDTH - 10):  # marginesy na boki
            if random.random() < 0.1:
                platformLength = random.randint(4, 7)
                valid = True

                # Sprawdź, czy cała przestrzeń dookoła platformy jest wolna
                for dx in range(-2, platformLength + 2):
                    px = x + dx
                    for dy in range(-2, 3):  # 2 kratki nad, 2 pod
                        py = y + dy
                        if 0 <= px < LEVEL_WIDTH and 0 <= py < LEVEL_HEIGHT:
                            if level[py][px] != '.':
                                valid = False
                                break
                    if not valid:
                        break

                # Jeśli miejsce wokół platformy jest czyste, twórz platformę
                if valid:
                    for dx in range(platformLength):
                        level[y][x + dx] = '#'

    # Przeciwnicy: E (zwykły), R (rzadszy)

    return level


def createRoomMap():
    grid = {}
    width, height = 6, 6
    x, y = 3, 3

    startRoom = Room("start", x, y)
    grid[(x, y)] = startRoom

    current = startRoom
    for _ in range(6):  # więcej niż 4!
        while True:
            dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])  # dodaj pionowe
            nx, ny = current.x + dx, current.y + dy
            if (nx, ny) not in grid and 0 <= nx < width and 0 <= ny < height:
                break
        newRoom = Room("enemy", nx, ny)
        grid[(nx, ny)] = newRoom
        current.connections.append(newRoom)
        newRoom.connections.append(current)
        current = newRoom

    current.room_type = "key"
    exitRoom = Room("exit", current.x + 1 if current.x + 1 < width else current.x - 1, current.y)
    grid[(exitRoom.x, exitRoom.y)] = exitRoom
    current.connections.append(exitRoom)
    exitRoom.connections.append(current)

    return grid

def add_passages(layout, directions):
    h = len(layout)
    w = len(layout[0])
    if 'left' in directions:
        layout[h // 2 - 1][0] = '.'
        layout[h // 2][0] = '.'
        layout[h // 2 - 1][1] = '.'
        layout[h // 2][1] = '.'

    if 'right' in directions:
        layout[h // 2 - 1][w - 1] = '.'
        layout[h // 2][w - 1] = '.'
        layout[h // 2 - 1][w - 2] = '.'
        layout[h // 2][w - 2] = '.'

    if 'top' in directions:
        layout[0][w // 2 - 1] = '.'
        layout[0][w // 2] = '.'
        layout[1][w // 2 - 1] = '.'
        layout[1][w // 2] = '.'

    if 'bottom' in directions:
        layout[h - 1][w // 2 - 1] = '.'
        layout[h - 1][w // 2] = '.'
        layout[h - 2][w // 2 - 1] = '.'
        layout[h - 2][w // 2] = '.'

    return layout


def stitchRoomsToLevel(grid):
    minX = min(r.x for r in grid.values())
    maxX = max(r.x for r in grid.values())
    minY = min(r.y for r in grid.values())
    maxY = max(r.y for r in grid.values())

    tileWidth = len(roomTemplates["start"][0][0])
    tileHeight = len(roomTemplates["start"][0])

    levelHeight = (maxY - minY + 1) * tileHeight
    levelWidth = (maxX - minX + 1) * tileWidth

    levelMap = [["#" for _ in range(levelWidth)] for _ in range(levelHeight)]

    for room in grid.values():
        # Pobierz losowy szablon i zamień na listę list (mutable)
        template = random.choice(roomTemplates[room.roomType])
        layout = [list(row) for row in template]

        # Ustal kierunki, w które prowadzą przejścia
        directions = set()
        for other in room.connections:
            dx = other.x - room.x
            dy = other.y - room.y
            if dx == 1:
                directions.add("right")
            elif dx == -1:
                directions.add("left")
            elif dy == 1:
                directions.add("bottom")
            elif dy == -1:
                directions.add("top")

        # Otwórz ściany – dodaj "." w odpowiednich miejscach
        if "left" in directions:
            layout[tileHeight // 2][0] = "."
            layout[tileHeight // 2][1] = "."
        if "right" in directions:
            layout[tileHeight // 2][-1] = "."
            layout[tileHeight // 2][-2] = "."
        if "top" in directions:
            layout[0][tileWidth // 2] = "."
            layout[1][tileWidth // 2] = "."
        if "bottom" in directions:
            layout[-1][tileWidth // 2] = "."
            layout[-2][tileWidth // 2] = "."

        # Pozycja w świecie
        startX = (room.x - minX) * tileWidth
        startY = (room.y - minY) * tileHeight

        # Wklej pokój do levelMap
        for y in range(tileHeight):
            for x in range(tileWidth):
                levelMap[startY + y][startX + x] = layout[y][x]

    # Zamień listę list znaków na listę stringów
    return ["".join(row) for row in levelMap]
def generatePlayableLevel(window, onLevelChange=None):
    roomMap = createRoomMap()
    levelLines = stitchRoomsToLevel(roomMap)
    return load_from_text_lines(levelLines, window, onLevelChange)
