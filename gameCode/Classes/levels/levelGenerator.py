import random
from collections import deque


class LevelGenerator:
    def __init__(self, width=80, height=50):
        self.width = width
        self.height = height

    def generatePassableLevelText(self):

        level = [["." for _ in range(self.width)] for _ in range(self.height)]
        self.addGround(level)
        floors = self.addFloors(level)
        self.addVerticalConnections(level, floors)
        self.addDecorations(level)
        self.addPlayerAndGoal(level, floors)
        self.addGround(level)
        return ["".join(row) for row in level]

    def addGround(self, level):
        groundY = self.height - 2
        current_height = groundY
        max_variation = 2  # maksymalne różnice wysokości
        smoothing = 0.7  # im wyższe, tym bardziej wyrównany teren

        for x in range(self.width):
            if random.random() < smoothing:
                delta = random.choice([-1, 0, 1])
                new_height = current_height + delta
                # Ograniczamy wysokość do bezpiecznego zakresu
                new_height = max(1, min(self.height - 3, new_height))
                current_height = new_height

            level[current_height][x] = "#"

            # Wypełniamy pod spodem (ziemię)
            for y in range(current_height + 1, self.height):
                level[y][x] = "#"

    def addPlatforms(self, level):
        num_platform_rows = random.randint(int(self.height // 3), int(self.width // 3))  # liczba platform do wygenerowania
        attempts = 0
        max_attempts = 100  # zapobiega nieskończonej pętli

        # Generowanie platform
        last_platform_y = self.height - 3  # Pierwsza platforma na poziomie gracza
        platform_rows = []

        while len(platform_rows) < num_platform_rows and attempts < max_attempts:
            # Generowanie wysokości platformy z minimalnym odstępem od poprzedniej
            min_y = max(last_platform_y - random.randint(2, 5), 2)  # Minimalna wysokość 2
            max_y = last_platform_y - 1  # Platforma musi być wyżej niż poprzednia

            # Zapewnienie, że min_y nie jest większe niż max_y
            if min_y > max_y:
                min_y = max_y

            y = random.randint(min_y, max_y)  # Losujemy pozycję Y platformy

            # Jeśli platforma jest zbyt blisko poprzedniej, próbuj ponownie
            if all(abs(y - r) > 2 for r in platform_rows):  # zapewnia odstęp w pionie
                platform_rows.append(y)
                last_platform_y = y
            attempts += 1

        # Sortowanie platform w kolejności od dołu do góry
        platform_rows = sorted(platform_rows, reverse=True)
        platforms = []
        for y in platform_rows:
            x = 2
            while x < self.width - 5:
                if random.random() < 0.7:  # 70% szans na stworzenie platformy
                    length = random.randint(4, 7)  # Losujemy długość platformy
                    if x + length >= self.width:
                        break
                    for i in range(length):
                        level[y][x + i] = "#"
                        above_y = y - 1
                        if above_y >= 0 and level[above_y][x + i] == ".":
                            if random.random() < 0.15:
                                level[above_y][x + i] = "C"
                            elif random.random() < 0.10:
                                level[above_y][x + i] = random.choice(["E", "R"])  # Dodajemy wrogów/obiekty
                    platforms.append((x, x + length - 1, y))  # Dodajemy platformę do listy
                    x += length + random.randint(2, 6)  # Przesuwamy pozycję x
                else:
                    x += random.randint(3, 6)  # Losujemy, gdzie może pojawić się kolejna platforma

        # Zapewnienie minimalnej odległości pomiędzy platformami, żeby były dostępne
        adjusted_platforms = []
        for i in range(1, len(platforms)):
            prev_x1, prev_x2, prev_y = platforms[i - 1]
            x1, x2, y = platforms[i]

            # Jeśli platformy są za daleko od siebie, przesuwamy platformę w górę
            if prev_y - y > 3:
                y = prev_y - 3  # Platforma będzie przesunięta w górę, aby była osiągalna

            adjusted_platforms.append((x1, x2, y))

        # Uaktualniamy listę platform
        platforms = adjusted_platforms

        return platforms
    def addVerticalConnections(self, level, platforms):
        platforms.sort(key=lambda p: p[2])  # Sortuj po Y od dołu
        for i in range(len(platforms) - 1):
            x1_left, x1_right, y1 = platforms[i]
            x2_left, x2_right, y2 = platforms[i + 1]
            common_left = max(x1_left, x2_left)
            common_right = min(x1_right, x2_right)

            if common_left <= common_right:
                mid_x = random.randint(common_left, common_right)
            else:
                mid_x = random.randint(x2_left + 1, x2_right - 1)

            for y in range(y1 - 1, y2, -1):
                if 0 <= y < self.height:
                    level[y][mid_x] = "#"

    def addFloors(self, level):
        floor_rows = []
        y = self.height - 4
        while y > 3:
            floor_rows.append(y)
            y -= random.randint(3, 5)

        floor_segments = []

        for y in floor_rows:
            x = 1
            while x < self.width - 2:
                if random.random() < 0.95:  # zwiększamy szansę na generowanie podłóg z 85% do 95%
                    length = random.randint(6, 12)  # trochę dłuższe platformy
                    for i in range(length):
                        if x + i < self.width - 1:
                            level[y][x + i] = "#"

                            # Dekoracje/monety
                            if random.random() < 0.1:
                                level[y - 1][x + i] = "C"
                            elif random.random() < 0.05:
                                level[y - 1][x + i] = random.choice(["E", "R"])

                            # Kolumny od dołu
                            if random.random() < 0.25:
                                col_height = random.randint(1, 3)
                                for j in range(1, col_height + 1):
                                    if y + j < self.height:
                                        level[y + j][x + i] = "#"

                    floor_segments.append((x, x + length - 1, y))
                    x += length + random.randint(1, 3)  # mniejsza przerwa między platformami
                else:
                    x += random.randint(2, 5)

            # Dodanie pomocniczych platform do skoku
            for seg_start, seg_end, y in floor_segments:
                if random.random() < 0.8 and y + 5 < self.height:  # nieco częściej
                    platform_width = random.choice([3, 4])
                    px = seg_end - random.randint(0, 2)
                    py = y + 3
                    if px + platform_width < self.width:
                        for i in range(platform_width):
                            level[py][px + i] = "#"
                        if random.random() < 0.3 and py - 1 > 0:
                            level[py - 1][px + platform_width // 2] = "C"

        # Dodanie pionowych przejść (2–3 zejścia) w losowych kolumnach
        num_connections = random.randint(2, 3)
        for _ in range(num_connections):
            col = random.randint(3, self.width - 4)
            for y in floor_rows:
                if y + 1 < self.height:
                    level[y][col] = "."  # wymazujemy fragment podłogi, by zrobić pionowy spadek
                if y + 1 < self.height:
                    level[y + 1][col] = "."  # dodatkowe pogłębienie

        return floor_segments

    def addPlayerAndGoal(self, level, platforms):
        if not platforms:
            return

        # Sortuj platformy rosnąco po Y (czyli od dołu do góry)
        platforms.sort(key=lambda p: p[2])

        # Gracz na najniższej platformie
        start_x = random.randint(platforms[0][0], platforms[0][1])
        start_y = platforms[0][2]
        level[start_y - 1][start_x] = "P"

        # Drzwi na najwyższej platformie
        end_x = random.randint(platforms[-1][0], platforms[-1][1])
        end_y = platforms[-1][2]
        level[end_y - 1][end_x] = "D"

        # Klucz – na losowej platformie między startem a końcem (jeśli są przynajmniej 3 poziomy)
        if len(platforms) >= 3:
            middle_platforms = platforms[1:-1]
            key_platform = random.choice(middle_platforms)
        else:
            key_platform = platforms[len(platforms) // 2]

        key_x = random.randint(key_platform[0], key_platform[1])
        key_y = key_platform[2]
        level[key_y - 1][key_x] = "K"

    def addDecorations(self, level):
        for _ in range(20):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 3)
            if level[y][x] == ".":
                level[y][x] = random.choice(["*", "T", "B"])
