import pygame

from gameCode.Classes.physicClass import Physic

class Projectile(Physic):
    def __init__(self,x,y, direction):
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

    def draw(self, window, cameraX, cameraY):
        if not self.active:
            return
        if self.direction > 0:
            pygame.draw.rect(window, (255, 255, 255), (self.positionX - cameraX, self.positionY - cameraY, 10, 10))
        else:
            pygame.draw.rect(window, (255, 255, 255), (self.positionX - cameraX, self.positionY - cameraY, 10, 10))
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

                        e.takeDamage(player.inventory.getSelectedWeapon().damage, player)
                        if e.health <= 0:
                            enemy.remove(e)
                        break