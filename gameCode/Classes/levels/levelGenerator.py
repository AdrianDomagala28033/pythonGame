import random

class LevelGenerator:
    def __init__(self, width=40, height=30):
        self.width = width
        self.height = height

    def generatePassableLevelText(self):
        level = [["." for _ in range(self.width)] for _ in range(self.height)]
        self.addGround(level)
        platforms = self.addPlatforms(level)
        self.addVerticalConnections(level, platforms)
        self.addDecorations(level)
        self.addPlayerAndGoal(level, platforms)
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
        num_platform_rows = random.randint(6, 10)  # liczba platform do wygenerowania
        used_rows = set()  # Zbiór do przechowywania pozycji platform
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
                        if random.random() < 0.15:
                            level[y - 1][x + i] = "C"  # Dodajemy monety
                        elif random.random() < 0.10:
                            level[y - 1][x + i] = random.choice(["E", "R"])  # Dodajemy wrogów/obiekty
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

    def addPlayerAndGoal(self, level, platforms):
        # Dodaj gracza nad jedną z dolnych platform (bliżej początku)
        if platforms:
            x1, x2, y = platforms[-1]  # najniższa platforma
            player_x = random.randint(x1, x2)
            level[y - 1][player_x] = "P"

        # Dodaj cel na jednej z górnych platform (bliżej końca)
        if len(platforms) >= 2:
            x1, x2, y = platforms[0]  # najwyższa platforma
            goal_x = random.randint(x1, x2)
            level[y - 1][goal_x] = "K"

    def addDecorations(self, level):
        for _ in range(20):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 3)
            if level[y][x] == ".":
                level[y][x] = random.choice(["*", "T", "B"])


