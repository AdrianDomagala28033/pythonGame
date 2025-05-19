import pygame

from gameCode.Classes.UI.minimap import drawMiniMap


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

    def getSelectedWeapon(self):
        return self.weaponSlots[self.selectedWeaponIndex]
    def getSelectedItem(self):
        return self.usableItems[self.selectedItemIndex]
    def getWeaponList(self):
        return self.weaponSlots

    def setItemList(self, itemList):
        self.usableItems = [None] * 4
        for i in range(min(4, len(itemList))):
            self.usableItems[i] = itemList[i]

    def setWeaponList(self, weaponList):
        self.weaponSlots = [None] * 2
        for i in range(min(2, len(weaponList))):
            self.weaponSlots[i] = weaponList[i]
    def getItemList(self):
        if self.usableItems != None:
            return self.usableItems
        else:
            return None
    def useItem(self, player):
        item = self.usableItems[self.selectedItemIndex]
        if item and item.usable:
            item.use(player)
            self.usableItems[self.selectedItemIndex] = None

    def drawInventory(self, window, x = 10, y=90):
        slotSize = 50
        spacing = 10

        for i, item in enumerate(self.usableItems):
            rect = pygame.Rect(x + i * (slotSize + spacing), y, slotSize, slotSize)
            pygame.draw.rect(window, (200, 200, 200), rect, 3, border_radius=5)
            if i == self.selectedItemIndex:
                pygame.draw.rect(window, (255, 255, 0), rect, 3, border_radius=5)
            if item:
                icon = pygame.image.load(item.icon)
                window.blit(icon, (rect.x, rect.y))
        y += slotSize + spacing + 10
        for i, weapon in enumerate(self.weaponSlots):
            rect = pygame.Rect(x + i * (slotSize + spacing), y, slotSize, slotSize)
            pygame.draw.rect(window, (180, 180, 180), rect, border_radius=5)
            if i == self.selectedWeaponIndex:
                pygame.draw.rect(window, (0, 255, 0), rect, 3, border_radius=5)
            if weapon:
                icon = pygame.image.load(weapon.image)
                window.blit(icon, (rect.x, rect.y))
