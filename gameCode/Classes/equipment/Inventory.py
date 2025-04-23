import pygame


class Inventory:
    def __init__(self):
        self.weaponSlots = [None] * 2
        self.usableItems = [None] * 4
        self.selectedItemIndex = 0
        self.selectedWeaponIndex = 0

    def addItem(self, item):
        for i in range(len(self.usableItems)):
            if self.usableItems[i] is None:
                self.usableItems[i] = item
                return True
        return False #znaczy że nie ma miejsca

    def addWeapon(self, weapon):
        for i in range(len(self.weaponSlots)):
            if self.weaponSlots[i] is None:
                self.weaponSlots[i] = weapon
                return True
        return False

    def useItem(self, player):
        item = self.usableItems[self.selectedItemIndex]
        if item:
            item.use(player)
            self.usableItems[self.selectedItemIndex] = None

    def drawInventory(self, window, x = 20, y=20):
        slotSize = 50
        spacing = 10
        font = pygame.font.SysFont("comicsans", 18)

        for i, item in enumerate(self.usableItems):
            rect = pygame.Rect(x + i * (slotSize + spacing), y, slotSize, slotSize)
            pygame.draw.rect(window, (200, 200, 200), rect, 3, border_radius=5)
            if i == self.selectedItemIndex:
                pygame.draw.rect(window, (255, 255, 0), rect, 3, border_radius=5)
            if item:
                text = font.render(item.name, True, (0, 0, 0))
                icon = pygame.image.load(item.icon)
                window.blit(icon, (rect.x, rect.y))
        y += slotSize + spacing + 10
        for i, weapon in enumerate(self.weaponSlots):
            rect = pygame.Rect(x + i * (slotSize + spacing), y, slotSize, slotSize)
            pygame.draw.rect(window, (180, 180, 180), rect, border_radius=5)
            if i == self.selectedWeaponIndex:
                pygame.draw.rect(window, (0, 255, 0), rect, 3, border_radius=5)
            if weapon:
                text = font.render(weapon.name, True, (0, 0, 0))
                window.blit(text, (rect.x + 5, rect.y + 5))