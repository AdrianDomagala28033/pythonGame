import pygame

from gameCode.Classes.levels.levelManagment.levelClass import Level
from gameCode.Classes.physicClass import Physic

class Projectile(Physic):
    def __init__(self,x,y, direction):
        self.image = pygame.image.load('./images/weapons/BasicArrow.PNG')
        super().__init__(x, y, self.image.get_width(), self.image.get_height(), 9, 7)
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

    def draw(self, window, cameraX, cameraY):
        if not self.active:
            return
        if self.direction > 0:
            window.blit(pygame.transform.scale2x(self.image), (self.positionX - cameraX - 30, self.positionY - cameraY - 10))
        else:
            window.blit(pygame.transform.flip(pygame.transform.scale2x(self.image), True, False), (self.positionX - cameraX - 50, self.positionY - cameraY -10))
        self.update()
    def bulletColision(self, player, enemy, obstacles):
        if player.inventory.getSelectedWeapon().tag == "bow":
            for arrow in player.inventory.getSelectedWeapon().projectiles:
                if not arrow.active:
                    continue
                for obj in obstacles:
                    if arrow.hitbox.colliderect(obj.hitbox):
                        arrow.active = False
                for e in enemy:
                    if arrow.hitbox.colliderect(e.hitbox):
                        arrow.active = False
                        baseDamage = player.inventory.getSelectedWeapon().getEffectiveDamage(player.level)
                        bonus = player.strength * 1
                        e.takeDamage(baseDamage + bonus, player)
                        break