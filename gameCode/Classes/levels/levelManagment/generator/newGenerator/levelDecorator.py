import random


def populateLevelContent(level, roomMap, width, height):
    enemyChars = ['E', 'R']
    maxEnemies = width // 4
    maxCoins = width // 3
    maxChests = width // 12

    placedEnemies = 0
    placedCoins = 0
    placedChests = 0
    placedKey = False
    placedDoor = False
    placedPlayer = False

    rooms = list(roomMap.items())
    random.shuffle(rooms)

    for (x, y), room in rooms:
        px, py = room['posX'], room['posY']
        w, h = room['width'], room['height']
        layout = room['layout']

        enemiesInRoom = 0
        coinsInRoom = 0
        chestsInRoom = 0

        roomMaxEnemies = random.randint(1, 2)
        roomMaxCoins = random.randint(2, 5)
        roomMaxChests = random.randint(0, 1)

        positions = [
            (dx, dy)
            for dy in range(1, h - 1)
            for dx in range(1, w - 1)
            if 0 <= px + dx < width - 1 and 0 <= py + dy < height - 1
        ]
        random.shuffle(positions)

        for dx, dy in positions:
            gx = px + dx
            gy = py + dy
            above = level[gy][gx]
            below = level[gy + 1][gx]

            # Spawn gracza w pokoju start
            if not placedPlayer and room['type'] == 'start' and above == '.' and below == '#':
                level[gy][gx] = 'P'
                placedPlayer = True
                continue

            # Drzwi tylko raz
            if not placedDoor and room['type'] == 'exit' and above == '.' and below == '#':
                level[gy][gx] = 'D'
                placedDoor = True
                continue

            # Klucz tylko raz
            if not placedKey and room['type'] == 'key' and above == '.' and below == '#':
                level[gy][gx] = 'K'
                placedKey = True
                continue

            # Skrzynka
            if placedChests < maxChests and chestsInRoom < roomMaxChests:
                if above == '.' and below == '#' and random.random() < 0.1:
                    level[gy][gx] = 'c'
                    placedChests += 1
                    chestsInRoom += 1
                    continue

            # Monety
            if placedCoins < maxCoins and coinsInRoom < roomMaxCoins:
                if above == '.' and random.random() < 0.2:
                    level[gy][gx] = 'C'
                    placedCoins += 1
                    coinsInRoom += 1
                    continue

            # Przeciwnik
            if placedEnemies < maxEnemies and enemiesInRoom < roomMaxEnemies:
                if above == '.' and below == '#' and random.random() < 0.15:
                    level[gy][gx] = random.choice(enemyChars)
                    placedEnemies += 1
                    enemiesInRoom += 1
                    continue

    return [''.join(row) for row in level]

def decorateWithPlatforms(level):
    height = len(level)
    width = len(level[0])
    level = [list(row) for row in level]
    for y in range(4, height - 4):
        for x in range(4, width - 10):
            if random.random() > 0.025:
                continue  # kontroluj gęstość platform

            platLen = random.randint(4, 6)

            # Zakres: [x, x+platLen), y
            valid = True

            for dx in range(platLen):
                px = x + dx

                for dy in [-2, -1, 1, 2]:  # 2 nad i 2 pod
                    py = y + dy
                    if not (0 <= px < width and 0 <= py < height):
                        valid = False
                        break
                    if level[py][px] != '.':
                        valid = False
                        break

                # środek platformy nie może już być zajęty
                if level[y][px] != '.':
                    valid = False

            if not valid:
                continue

            # dodatkowo: sprawdź czy pod platformą nie ma innej platformy w promieniu 2
            underOk = True
            for dx in range(platLen):
                for dy in range(1, 3):  # y+1, y+2
                    if level[y + dy][x + dx] == '#':
                        underOk = False
            if not underOk:
                continue

            # wszystko OK → stwórz platformę
            for dx in range(platLen):
                level[y][x + dx] = '#'

    return [''.join(row) for row in level]


def decorateWithMicroRooms(level):
    height = len(level)
    width = len(level[0])
    level = [list(row) for row in level]
    roomCount = 0

    for _ in range(50):  # maksymalna liczba mikro-pokoików
        roomW = random.choice([5, 6, 7])
        roomH = random.choice([4, 5, 6])
        rx = random.randint(3, width - roomW - 3)
        ry = random.randint(3, height - roomH - 3)

        # sprawdź czy cała przestrzeń jest pusta (lub powietrze)
        valid = True
        for dy in range(roomH):
            for dx in range(roomW):
                if level[ry + dy][rx + dx] != '.':
                    valid = False
        if not valid:
            continue

        # wygeneruj „pokój”
        for dy in range(roomH):
            for dx in range(roomW):
                if dy == 0 or dy == roomH - 1 or dx == 0 or dx == roomW - 1:
                    level[ry + dy][rx + dx] = '#'
                else:
                    level[ry + dy][rx + dx] = '.'

        # wejście — np. od góry
        entryX = rx + roomW // 2
        level[ry][entryX] = '.'
        level[ry - 1][entryX] = '.'

        # zawartość (losowa)
        cx = rx + roomW // 2
        cy = ry + roomH // 2

        content = random.choices(['c', 'C', 'C', 'Q', '^', '.'], [0.3, 0.4, 0.2, 0.05, 0.05, 0.05])[0]
        level[cy][cx] = content

        roomCount += 1
        if roomCount >= 10:
            break

    return [''.join(row) for row in level]

