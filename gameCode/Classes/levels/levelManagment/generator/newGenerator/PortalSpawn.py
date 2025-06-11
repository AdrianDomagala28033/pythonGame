import pygame


class PortalSpawn:
    def __init__(self, x, y, onReturnToHub):
        self.positionX = x
        self.positionY = y
        self.image = pygame.image.load("./images/portalSpawn.png") # lub coś tymczasowego
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.promptFont = pygame.font.SysFont("arial", 18)
        self.promptText = self.promptFont.render("Wciśnij E, aby wrócić do huba", True, (255, 255, 255))
        self.visible = False
        self.onReturnToHub = onReturnToHub

    def tick(self, player):
        self.visible = self.hitbox.colliderect(player.hitbox)
        if self.visible and player.wantInteract:
            print("↩️ Wracanie do huba...")
            if self.onReturnToHub:
                self.onReturnToHub()

    def draw(self, window, cameraX, cameraY):
        window.blit(self.image, (self.positionX - cameraX, self.positionY - cameraY))
        if self.visible:
            window.blit(self.promptText, (self.positionX - cameraX, self.positionY - cameraY - 30))
