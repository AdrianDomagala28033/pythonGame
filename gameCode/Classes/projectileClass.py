import pygame

from gameCode.Classes.physicClass import Physic

class Projectile(Physic):
    def __init__(self,x,y, direction, window):
        super().__init__(x, y, 5, 2, 5, 7)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Tworzymy przezroczysty Surface
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 10, 10))
        self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        self.direction = direction
        self.tag = "projectile"
        self.active = True

    def update(self):
        if(self.direction > 0):
            self.positionX += self.acc
            self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        else:
            self.positionX -= self.acc
            self.hitbox = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        if not self.active:
            return

    def off_screen(self):
        return self.positionX < 0 or self.positionX > 800  # dostosuj do wielkości ekranu

    def draw(self, window):
        if not self.active:
            return  # nie rysuj nieaktywnej strzały

        if self.direction > 0:
            pygame.draw.rect(window, (255, 0, 0), (self.positionX, self.positionY + 30, 10, 10))
        else:
            pygame.draw.rect(window, (255, 0, 0), (self.positionX, self.positionY + 30, 10, 10))
        self.update()
    def bulletColision(self, player, enemy):
        for arrow in player.distanceWeapon.projectiles:
            if not arrow.active:
                continue
            for e in enemy:
                if arrow.hitbox.colliderect(e.hitbox):
                    arrow.active = False
                    e.health -= player.distanceWeapon.damage
                    if e.health <= 0:
                        enemy.remove(e)
                    break