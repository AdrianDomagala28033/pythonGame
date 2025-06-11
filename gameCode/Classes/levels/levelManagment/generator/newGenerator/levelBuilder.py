import random

from gameCode.Classes.levels.levelManagment.generator.newGenerator.levelDecorator import populateLevelContent, \
    decorateWithMicroRooms, decorateWithPlatforms
from gameCode.Classes.levels.levelManagment.generator.newGenerator.roomGenerator import generateRoom
def digTunnel(level, x1, y1, x2, y2):
    x, y = x1, y1
    while x != x2:
        level[y][x] = '.'
        x += 1 if x2 > x else -1
    while y != y2:
        level[y][x] = '.'
        y += 1 if y2 > y else -1
    level[y][x] = '.'
def stitchRoomsDynamic(roomMap):
    colWidths = {}
    rowHeights = {}
    for (x, y), data in roomMap.items():
        exits = []
        for (nx, ny) in data['connections']:
            if nx > x: exits.append('right')
            if nx < x: exits.append('left')
            if ny > y: exits.append('bottom')
            if ny < y: exits.append('top')

        layout, w, h = generateRoom(data['type'], set(exits))
        data.update({'layout': layout, 'width': w, 'height': h})
        colWidths[x] = max(colWidths.get(x, 0), w)

        rowHeights[y] = max(rowHeights.get(y, 0), h)

    colOffsets, rowOffsets = {}, {}
    currentX, currentY = 0, 0
    for x in sorted(colWidths):
        colOffsets[x] = currentX
        currentX += colWidths[x]  # 🔧 spacing removed

    for y in sorted(rowHeights):
        rowOffsets[y] = currentY
        currentY += rowHeights[y]

    totalW, totalH = currentX, currentY
    level = [['#' for _ in range(totalW)] for _ in range(totalH)]

    for (x, y), data in roomMap.items():
        for (nx, ny) in data['connections']:
            if (nx, ny) <= (x, y):
                continue
            A = data
            B = roomMap[(nx, ny)]
            print(A)
            print(list(A['connections']))
            a = list(A['connections'])[0]
            print(f"Parametr {a[0]}")
            ax, ay = A['connections'], A['connections']
            aw, ah = A['width'], A['height']
            bx, by = B['connections'], B['connections']
            bw, bh = B['width'], B['height']

            if nx > x:
                x1 = ax + aw - 1
                y1 = ay + ah // 2
                x2 = bx
                y2 = by + bh // 2
            elif nx < x:
                x1 = ax
                y1 = ay + ah // 2
                x2 = bx + bw - 1
                y2 = by + bh // 2
            elif ny > y:
                x1 = ax + aw // 2
                y1 = ay + ah - 1
                x2 = bx + bw // 2
                y2 = by
            else:  # ny < y
                x1 = ax + aw // 2
                y1 = ay
                x2 = bx + bw // 2
                y2 = by + bh - 1

            digTunnel(level, x1, y1, x2, y2)
    return [''.join(line) for line in level]

def stitchRooms(roomMap):
    roomWidth = 20
    roomHeight = 12

    minX = min(x for x, y in roomMap)
    maxX = max(x for x, y in roomMap)
    minY = min(y for x, y in roomMap)
    maxY = max(y for x, y in roomMap)

    totalWidth = (maxX - minX + 1) * roomWidth
    totalHeight = (maxY - minY + 1) * roomHeight

    level = [['#' for _ in range(totalWidth)] for _ in range(totalHeight)]

    for (x, y), data in roomMap.items():
        exits = []
        for cx, cy in data['connections']:
            if cx > x: exits.append('right')
            if cx < x: exits.append('left')
            if cy > y: exits.append('bottom')
            if cy < y: exits.append('top')

        layout = generateRoom(data['type'], set(exits))
        baseX = (x - minX) * roomWidth
        baseY = (y - minY) * roomHeight

        for dy, line in enumerate(layout):
            for dx, char in enumerate(line):
                level[baseY + dy][baseX + dx] = char

    return [''.join(row) for row in level]

def stitchRoomsNatural(roomMap, width=random.randint(100, 180), height=random.randint(30, 80)):
    level = [['#' for _ in range(width)] for _ in range(height)]
    used_positions = []
    min_distance = 10  # minimalna odległość między pokojami

    # 1. Nadaj każdemu pokojowi losową pozycję z zachowaniem dystansu
    for (x, y), data in roomMap.items():
        # Szukaj pozycji tak długo, aż nie będzie za blisko innych
        for _ in range(100):
            posX = random.randint(4, width - 30)
            posY = random.randint(3, height - 15)
            too_close = False
            for ox, oy in used_positions:
                if abs(posX - ox) < min_distance and abs(posY - oy) < min_distance:
                    too_close = True
                    break
            if not too_close:
                break

        used_positions.append((posX, posY))
        data["posX"] = posX
        data["posY"] = posY

        exits = []
        for (nx, ny) in data['connections']:
            if nx > x: exits.append('right')
            if nx < x: exits.append('left')
            if ny > y: exits.append('bottom')
            if ny < y: exits.append('top')

        layout, w, h = generateRoom(data['type'], set(exits))
        data.update({'layout': layout, 'width': w, 'height': h})

        # Wstaw layout do mapy
        for rowIdx, row in enumerate(layout):
            for colIdx, char in enumerate(row):
                tx = posX + colIdx
                ty = posY + rowIdx
                if 0 <= tx < width and 0 <= ty < height:
                    if char != ' ':
                        level[ty][tx] = char

    # 2. Połącz pokoje organiczną ścieżką
    def digOrganicPath(x1, y1, x2, y2):
        x, y = x1, y1
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        # poziome przejścia (klasyczne)
        if abs(x2 - x1) > abs(y2 - y1):
            while x != x2:
                for d in range(-1, 2):
                    if 0 <= y + d < len(level) and 0 <= x < len(level[0]):
                        level[y + d][x] = '.'
                x += dx
            while y != y2:
                for d in range(-1, 2):
                    if 0 <= x + d < len(level[0]) and 0 <= y < len(level):
                        level[y][x + d] = '.'
                y += dy

        # pionowe przejście z platformami
        else:
            midX = x
            while y != y2:
                # Wyczyść pionowy korytarz
                for d in range(-1, 2):
                    if 0 <= x + d < len(level[0]) and 0 <= y < len(level):
                        level[y][x + d] = '.'

                # Co kilka kroków dodaj platformę
                if y % 4 == 0:
                    for px in range(-2, 3):
                        if 0 <= x + px < len(level[0]) and 0 <= y < len(level):
                            level[y][x + px] = '#'
                    # zostaw dziurę w środku
                    level[y][x] = '.'

                y += dy

            # końcówka – połączenie poziome jeśli trzeba
            while x != x2:
                for d in range(-1, 2):
                    if 0 <= y + d < len(level) and 0 <= x < len(level[0]):
                        level[y + d][x] = '.'
                x += dx

    for (x, y), room in roomMap.items():
        for (nx, ny) in room['connections']:
            if (nx, ny) <= (x, y): continue
            a = room
            b = roomMap[(nx, ny)]

            ax = a['posX'] + a['width'] // 2
            ay = a['posY'] + a['height'] // 2
            bx = b['posX'] + b['width'] // 2
            by = b['posY'] + b['height'] // 2

            digOrganicPath(ax, ay, bx, by)

    # 3. Ramka (opcjonalna)
    for x in range(width):
        level[0][x] = level[-1][x] = '#'
    for y in range(height):
        level[y][0] = level[y][-1] = '#'
    level = populateLevelContent(level, roomMap, width, height)
    level = decorateWithPlatforms(level)
    return [''.join(row) for row in level]
