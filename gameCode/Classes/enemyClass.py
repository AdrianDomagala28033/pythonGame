import pygame

from gameCode.Classes.physicClass import Physic

class Enemy(Physic):
    def __init__(self, x, y, image):
        self.image = image
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height, 2, 5)
        self.health = 100
        self.damage = 10
        self.direction = 1
        self.startPosition = x
        self.lastTriggerTime = 0
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.tag = "enemy"

    def tick(self, player, enemy, window):
        self.move(player, enemy)
        self.physicTick(player)
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)


    def draw(self, window):
        self.changeDirection(window)
        self.healthBar(window)
    def move(self, player, enemy):
        currentTime = pygame.time.get_ticks()
        cooldown = 500
        self.positionX -= self.acc * self.direction
        if(self.positionX == self.startPosition - 200):
            self.direction *= -1
        elif(self.positionX == self.startPosition + 200):
            self.direction *= -1
        elif(self.hitbox.colliderect(player.hitbox) and currentTime - self.lastTriggerTime >= cooldown):
            self.direction *= -1
            self.lastTriggerTime = currentTime


    def changeDirection(self, window):
        if (self.direction > 0):
            window.blit(self.image, (self.positionX, self.positionY))
        else:
            window.blit(pygame.transform.flip(self.image, True, False),
                        (self.positionX, self.positionY))

    def healthBar(self, window):
        pygame.draw.rect(window, (235, 64, 52), (self.positionX, self.positionY - 10, self.width * (self.health / 100), 10))


