import pygame

class Door:
    def __init__(self, x, y):
        self.positionX = x
        self.positionY = y
        self.image = pygame.image.load("./images/door.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.visionRange = 100

    def tick(self, player):
        self.detectPlayer(player)
        if player.hitbox.colliderect(self.hitbox) and player.hasKey == True:
            pass


    def draw(self, window, cameraX):
        window.blit(self.image, (self.positionX - cameraX, self.positionY - 30))

    def detectPlayer(self, player):
        rightVision = pygame.Rect(self.positionX, self.positionY, self.visionRange, self.height)
        leftVision = pygame.Rect(self.positionX - self.visionRange, self.positionY, self.visionRange, self.height)


        if rightVision.colliderect(player.hitbox) or leftVision.colliderect(player.hitbox):
            self.image = pygame.image.load("./images/doorOpen.png")
        else:
            self.image = pygame.image.load("./images/door.png")

