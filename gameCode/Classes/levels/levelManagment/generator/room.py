import random


class Room:
    def __init__(self, roomType="noraml", x=0, y=0):
        self.roomType = roomType
        self.connections = []
        self.x = x
        self.y = y

    def generateLayout(self, width=20, height=10):
        layout = [['#'] * width for _ in range(height)]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                layout[y][x] = '.' if random.random() > 0.1 else '#'

        # Dodaj jakieś obiekty:
        if self.roomType == "key":
            layout[height // 2][width // 2] = 'K'
        elif self.roomType == "exit":
            layout[height // 2][width // 2] = 'D'
        elif self.roomType == "start":
            layout[height // 2][width // 2] = 'P'

        return layout