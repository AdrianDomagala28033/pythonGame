import random
from perlin_noise import PerlinNoise
import networkx as nx

class LevelGenerator:
    def __init__(self, width=100, height=50, roomCount=20):
        self.width = width
        self.height = height
        self.roomCount = roomCount
        self.noise = PerlinNoise(octaves=4)

    def createEmptyMap(self):
        return [["#" for _ in range(self.width)] for _ in range(self.height)]

    def generateNoiseLayer(self):
        level = self.createEmptyMap()
        for y in range(self.height):
            for x in range(self.width):
                val = self.noise([x / self.width, y / self.height])
                if val > 0.05:
                    level[y][x] = "."
        return level

    def placeRooms(self, level):
        rooms = []
        for _ in range(self.roomCount):
            rw, rh = random.randint(6, 10), random.randint(4, 6)
            rx = random.randint(1, self.width - rw - 1)
            ry = random.randint(1, self.height - rh - 1)
            rooms.append({'x': rx, 'y': ry, 'w': rw, 'h': rh})
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    level[y][x] = "."
        return rooms

    def connectRoomsGraph(self, level, rooms):
        G = nx.Graph()
        for i, room in enumerate(rooms):
            cx = room['x'] + room['w'] // 2
            cy = room['y'] + room['h'] // 2
            G.add_node(i, pos=(cx, cy))

        for i in range(len(rooms)):
            for j in range(i + 1, len(rooms)):
                x1, y1 = G.nodes[i]['pos']
                x2, y2 = G.nodes[j]['pos']
                dist = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
                G.add_edge(i, j, weight=dist)

        mst = nx.minimum_spanning_tree(G)
        for u, v in mst.edges:
            self.digTunnel(level, G.nodes[u]['pos'], G.nodes[v]['pos'])

    def digTunnel(self, level, start, end, pathWidth=2):
        x1, y1 = start
        x2, y2 = end

        points = [(x1, y1)]
        steps = max(abs(x2 - x1), abs(y2 - y1))

        for i in range(1, steps):
            t = i / steps
            # interpolacja z lekkim zakrzywieniem (np. sinusoida + szum)
            xt = int(x1 + t * (x2 - x1) + random.randint(-1, 1))
            yt = int(y1 + t * (y2 - y1) + random.choice([-1, 0, 1]))
            points.append((xt, yt))

        points.append((x2, y2))

        for (px, py) in points:
            for dx in range(-pathWidth // 2, pathWidth // 2 + 1):
                for dy in range(-pathWidth // 2, pathWidth // 2 + 1):
                    nx, ny = px + dx, py + dy
                    if 1 <= ny < self.height - 1 and 1 <= nx < self.width - 1:
                        level[ny][nx] = "."

    def placePlayerAndGoal(self, level, rooms):
        playerRoom = random.choice(rooms)
        px = playerRoom['x'] + playerRoom['w'] // 2
        py = playerRoom['y'] + playerRoom['h'] // 2
        level[py][px] = 'P'

        while True:
            doorRoom = random.choice(rooms)
            if doorRoom != playerRoom:
                dx = doorRoom['x'] + doorRoom['w'] // 2
                dy = doorRoom['y'] + doorRoom['h'] // 2
                if level[dy][dx] == ".":
                    level[dy][dx] = 'D'
                    break

    def generateLevel(self):
        level = self.generateNoiseLayer()
        rooms = self.placeRooms(level)
        self.connectRoomsGraph(level, rooms)
        self.placePlayerAndGoal(level, rooms)
        self.addPlatforms(level)
        self.addDistributedPlatforms(level)
        self.ensureAccessibility(level, rooms)
        self.addBottomWall(level)
        self.detectAndFixUnreachableAreas(level)
        return ["".join(row) for row in level]

    def addBottomWall(self, level):
        """Zamienia ostatni rząd na poziomą linię ściany (#)."""
        level[-1] = ["#"] * self.width

    def addPlatforms(self, level, windowSize=9, minEmptyRatio=0.85, platformLengthRange=(2, 4)):
        for y in range(1, self.height - windowSize - 1):
            for x in range(1, self.width - windowSize - 1):
                emptyCount = 0
                for dy in range(windowSize):
                    for dx in range(windowSize):
                        if level[y + dy][x + dx] == ".":
                            emptyCount += 1

                total = windowSize * windowSize
                if emptyCount / total >= minEmptyRatio:
                    # Umieść platformę na środku tego obszaru
                    platY = y + windowSize // 2
                    platX = x + windowSize // 2
                    platLen = random.randint(*platformLengthRange)
                    half = platLen // 2

                    for dx in range(-half, half + 1):
                        px = platX + dx
                        if 0 <= px < self.width and level[platY][px] == ".":
                            level[platY][px] = "#"

    def addDistributedPlatforms(self, level, sectorsX=10, sectorsY=5, attemptsPerSector=2, minLength=4, maxLength=8):
        sectorWidth = self.width // sectorsX
        sectorHeight = self.height // sectorsY

        for sy in range(sectorsY):
            for sx in range(sectorsX):
                for _ in range(attemptsPerSector):
                    length = random.randint(minLength, maxLength)
                    x_min = sx * sectorWidth + 1
                    x_max = min((sx + 1) * sectorWidth - length - 2, self.width - length - 1)
                    y_min = sy * sectorHeight + 2
                    y_max = min((sy + 1) * sectorHeight - 2, self.height - 2)

                    if x_min >= x_max or y_min >= y_max:
                        continue  # pomiń ten sektor, jeśli za mały

                    x = random.randint(x_min, x_max)
                    y = random.randint(y_min, y_max)

                    # Sprawdź czy można umieścić platformę
                    canPlace = True
                    for i in range(length):
                        if level[y][x + i] != ".":
                            canPlace = False
                            break
                        for dy in range(1, 4):
                            if y + dy >= self.height or level[y + dy][x + i] == "#":
                                canPlace = False
                                break
                        if not canPlace:
                            break

                    if canPlace:
                        for i in range(length):
                            level[y][x + i] = "#"

    def ensureAccessibility(self, level, rooms, platform_interval=3, platform_length=5):
        from collections import deque

        # Znajdź pozycję gracza
        for y in range(self.height):
            for x in range(self.width):
                if level[y][x] == "P":
                    playerPos = (x, y)
                    break

        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        queue = deque([playerPos])
        visited[playerPos[1]][playerPos[0]] = True

        # BFS - zaznacz dostępne kratki
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not visited[ny][nx] and level[ny][nx] in (".", "P", "D", "#"):
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        # Sprawdź które pokoje są niedostępne
        for room in rooms:
            cx = room['x'] + room['w'] // 2
            cy = room['y'] + room['h'] // 2
            if not visited[cy][cx]:
                # Znajdź najbliższy dostępny punkt
                best = None
                bestDist = float("inf")
                for y in range(self.height):
                    for x in range(self.width):
                        if visited[y][x] and level[y][x] == ".":
                            dist = abs(cx - x) + abs(cy - y)
                            if dist < bestDist:
                                best = (x, y)
                                bestDist = dist

                if best:
                    # Pokój znajduje się wyżej niż dostępny obszar → szyb z platformami
                    if cy < best[1] - 3:
                        for y in range(cy, best[1] + 1):
                            if 1 <= y < self.height - 1 and 1 <= cx < self.width - 1:
                                level[y][cx] = "."  # szyb

                                if (y - cy) % platform_interval == 0:
                                    # Dodaj platformę poziomą (np. 5-kratkową)
                                    start = max(1, cx - platform_length // 2)
                                    end = min(self.width - 2, start + platform_length)
                                    for px in range(start, end):
                                        level[y][px] = "#"
                    else:
                        # Normalny tunel jeśli nie trzeba wspinać się
                        self.digTunnel(level, (cx, cy), best)

    def detectAndFixUnreachableAreas(self, level, maxJumpHeight=3, maxStepWidth=3, maxPlatforms=90):
        from collections import deque

        height = len(level)
        width = len(level[0])
        visited = [[False for _ in range(width)] for _ in range(height)]

        # Znajdź gracza
        for y in range(height):
            for x in range(width):
                if level[y][x] == 'P':
                    start = (x, y)
                    break
            else:
                continue
            break
        else:
            return

        # BFS – gdzie gracz może się dostać
        queue = deque([start])
        visited[start[1]][start[0]] = True

        while queue:
            x, y = queue.popleft()
            for dx in range(-maxStepWidth, maxStepWidth + 1):
                for dy in range(-maxJumpHeight, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if not visited[ny][nx] and level[ny][nx] == ".":
                            # Można stanąć jeśli ma coś pod spodem
                            if ny + 1 < height and level[ny + 1][nx] in ("#", "P", "D"):
                                visited[ny][nx] = True
                                queue.append((nx, ny))

        # Dodaj platformy tam, gdzie można pomóc doskoczyć
        platformsPlaced = 0
        for y in range(height - 4, 2, -1):
            for x in range(2, width - 2):
                if platformsPlaced >= maxPlatforms:
                    return

                if level[y][x] != "." or visited[y][x]:
                    continue

                # Czy nad tym miejscem jest pusta przestrzeń?
                if all(level[y - i][x] == "." for i in range(1, maxJumpHeight + 1)):
                    # Czy w pobliżu (w poziomie) jest jakieś dostępne pole niżej?
                    for dx in range(-maxStepWidth * 2, maxStepWidth * 2 + 1):
                        tx = x + dx
                        if 1 <= tx < width - 1 and visited[y + 1][tx]:
                            # Postaw krótką platformę
                            for i in range(-1, 2):
                                if 0 <= x + i < width and level[y][x + i] == ".":
                                    level[y][x + i] = "#"
                            platformsPlaced += 1
                            break
