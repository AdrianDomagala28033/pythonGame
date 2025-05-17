import pygame

from gameCode.Classes.UI.Item import Item


class Key(Item):
    def __init__(self, x, y):
        self.positionX = x
        self.positionY = y
        self.image = pygame.image.load("./images/key.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        super().__init__("key", "klucz do otwarcia drzwi",0, "key", "./images/key.png", None, False)
        self.collected = False
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

    def tick(self, player):
        self.check_collision(player)

    def draw(self, window, cameraX, cameraY):
        if not self.collected:
            window.blit(self.image, (self.positionX - cameraX, self.positionY - cameraY))

    def check_collision(self, player):
        if not self.collected and self.hitbox.colliderect(player.hitbox):
            self.collected = True
            player.hasKey = True
            player.inventory.addItem(self)
