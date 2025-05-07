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
        self.addBottomBorder(level)
        return ["".join(row) for row in level]

    def addGround(self, level):
        groundY = self.height - 2
        for x in range(self.width):
            level[groundY][x] = "#"

    def addPlatforms(self, level):
        platforms = []
        y = self.height - 6
        while y > 2:
            num_platforms = random.randint(2, 4)
            for _ in range(num_platforms):
                plat_x = random.randint(1, self.width - 8)
                plat_len = random.randint(4, 8)
                for i in range(plat_len):
                    if plat_x + i < self.width:
                        level[y][plat_x + i] = "#"
                platforms.append((plat_x, plat_x + plat_len - 1, y))
            y -= random.randint(3, 4)
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
        bottom_y = self.height - 3
        level[bottom_y][2] = "P"

        # Umieść drzwi i klucz na jednej z górnych platform
        goal_platform = platforms[-1]
        kx = random.randint(goal_platform[0] + 1, goal_platform[1] - 1)
        ky = goal_platform[2] - 1
        level[ky][kx] = "K"
        level[ky][min(kx + 2, self.width - 2)] = "D"

    def addDecorations(self, level):
        for _ in range(20):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 3)
            if level[y][x] == ".":
                level[y][x] = random.choice(["*", "T", "B"])

    def addBottomBorder(self, level):
        for x in range(self.width):
            level[self.height - 1][x] = "#"
