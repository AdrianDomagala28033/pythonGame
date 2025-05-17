import pygame



class Door:
    def __init__(self, x=0, y=0):
        self.positionX = x
        self.positionY = y
        self.images = [pygame.image.load(f"./images/doorAnimation/door{x}.png") for x in range(6)]  # lista obrazów
        self.image = self.images[0]  # aktualna klatka
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.visionRange = 100
        self.doorIndex = 0
        self.onLevelChange = None

    def tick(self, player, window):
        self.detectPlayer(player)
        if self.hitbox.colliderect(player.hitbox) and player.hasKey:
            item = player.inventory.getSelectedItem()
            if item is not None and item.name == "key":
                item.usable = True
                if self.onLevelChange:
                    item.use(player)
                    print("Wywołuję onLevelChange:", self.onLevelChange)
                    self.onLevelChange()
            else:
                return True
        return False

    def draw(self, window, cameraX, cameraY):
        window.blit(self.image, (self.positionX - cameraX, self.positionY - 30 - cameraY))

    def detectPlayer(self, player):
        rightVision = pygame.Rect(self.positionX, self.positionY, self.visionRange, self.height)
        leftVision = pygame.Rect(self.positionX - self.visionRange, self.positionY, self.visionRange, self.height)

        if rightVision.colliderect(player.hitbox) or leftVision.colliderect(player.hitbox):
            self.doorIndex += 0.3
            if self.doorIndex >= len(self.images):
                self.doorIndex = len(self.images) - 1
        else:
            self.doorIndex -= 0.3
            if self.doorIndex < 0:
                self.doorIndex = 0

        self.image = self.images[int(self.doorIndex)]
