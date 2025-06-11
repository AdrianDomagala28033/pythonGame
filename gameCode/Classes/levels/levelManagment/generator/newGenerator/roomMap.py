import random


def generateRoomMap(width, height):
    roomMap = {}
    startX, startY = width // 2, height // 2
    startPos = (startX, startY)
    queue = [startPos]
    roomMap[startPos] = {'type': 'start', 'connections': set()}

    # Twórz ścieżkę główną
    for _ in range(20):
        if not queue:
            break
        x, y = queue.pop(0)
        random.shuffle(DIRS := [(1, 0), (-1, 0), (0, 1), (0, -1)])
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in roomMap and 0 <= nx < width and 0 <= ny < height:
                roomMap[(nx, ny)] = {'type': 'enemy', 'connections': set()}
                roomMap[(x, y)]['connections'].add((nx, ny))
                roomMap[(nx, ny)]['connections'].add((x, y))
                queue.append((nx, ny))
                if random.random() < 0.6:  # dodaj 60% szansy na dodatkowe odgałęzienie
                    queue.append((nx, ny))
                break

    if len(roomMap) >= 5:
        last = list(roomMap.keys())[-1]
        roomMap[last]['type'] = 'exit'
        enemies = [k for k in roomMap if roomMap[k]['type'] == 'enemy']
        if enemies:
            keyRoom = random.choice(enemies)
            roomMap[keyRoom]['type'] = 'key'
            enemies.remove(keyRoom)
        for pos in enemies:
            if random.random() < 0.3:
                roomMap[pos]['type'] = random.choice(['loot', 'shop', 'quest'])

        # Secret
        for x in range(width):
            for y in range(height):
                if (x, y) not in roomMap:
                    roomMap[(x, y)] = {'type': 'secret', 'connections': set()}
                    break
            else:
                continue
            break

    return roomMap
