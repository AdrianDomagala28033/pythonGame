import pygame

from gameCode.Classes.UI.Inventory import Inventory
from gameCode.fonts.fonts import addFont


class ChestInventory(Inventory):
    def __init__(self):
        super().__init__()
        self.weaponSlots = [None] * 4
        self.usableItems = [None] * 4



class InventoryUiExchange:
    def __init__(self, playerInventory, chestInventory):
        self.playerInventory = playerInventory
        self.chestInventory = chestInventory
        self.active = False
        self.selectedSlot = None

    def toggle(self):
        self.active = not self.active

    def handleClick(self, pos):
        slotSize = 50
        spacing = 10

        # === OBSŁUGA USABLE ITEMS ===
        for invType, slots, y in [
            ("player", self.playerInventory.usableItems, 100),
            ("chest", self.chestInventory.usableItems, 300)
        ]:
            for i, item in enumerate(slots):
                x = 1000 + i * (slotSize + spacing)
                rect = pygame.Rect(x, y, slotSize, slotSize)
                if rect.collidepoint(pos) and item:
                    if invType == "chest":
                        success = self.playerInventory.addItem(item)
                        if success:
                            self.chestInventory.usableItems[i] = None
                    elif invType == "player":
                        success = self.chestInventory.addItem(item)
                        if success:
                            self.playerInventory.usableItems[i] = None
                    return  # zakończ po kliknięciu

        # === OBSŁUGA WEAPON SLOTS ===
        for invType, slots, y in [
            ("player", self.playerInventory.weaponSlots, 200),
            ("chest", self.chestInventory.weaponSlots, 400)
        ]:
            for i, weapon in enumerate(slots):
                x = 1000 + i * (slotSize + spacing)
                rect = pygame.Rect(x, y, slotSize, slotSize)
                if rect.collidepoint(pos) and weapon:
                    if invType == "chest":
                        success = self.playerInventory.addWeapon(weapon)
                        if success:
                            self.chestInventory.weaponSlots[i] = None
                    elif invType == "player":
                        success = self.chestInventory.addWeapon(weapon)
                        if success:
                            self.playerInventory.weaponSlots[i] = None
                    return

    def draw(self, window):
        tooltipCandidate = None
        tooltipPos = (0,0)
        mouseX, mouseY = pygame.mouse.get_pos()
        if not self.active:
            return
        font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 18)
        pygame.draw.rect(window, (30,30,30), (950, 80, 700, 400))

        slotSize = 50
        spacing = 10

        for invType, slots, y in [
            ("player", self.playerInventory.usableItems, 100),
            ("chest", self.chestInventory.usableItems, 300)
        ]:
            label = font.render(f'{invType.capitalize()} Items', True, (255, 255, 255))
            window.blit(label, (1000, y - 25))
            for i, item in enumerate(slots):
                x = 1000 + i * (slotSize + spacing)
                rect = pygame.Rect(x, y, slotSize, slotSize)
                pygame.draw.rect(window, (150, 150, 150), rect, 2)
                if item:
                    icon = pygame.image.load(item.icon)
                    window.blit(icon, (x, y))
                    if pygame.Rect(x,y, slotSize, slotSize).collidepoint(mouseX, mouseY):
                        tooltipCandidate = item
                        tooltipPos = (x,y)

        for invType, slots, y in [
            ("player", self.playerInventory.weaponSlots, 200),
            ("chest", self.chestInventory.weaponSlots, 400)
        ]:
            label = font.render(f'{invType.capitalize()} Weapons', True, (255, 255, 255))
            window.blit(label, (1000, y - 25))
            for i, weapon in enumerate(slots):
                x = 1000 + i * (slotSize + spacing)
                rect = pygame.Rect(x, y, slotSize, slotSize)
                pygame.draw.rect(window, (100, 100, 100), rect, 2)
                if weapon:
                    if isinstance(weapon.image, pygame.Surface):
                        icon = pygame.transform.scale(weapon.image, (50, 50))
                    else:
                        icon = pygame.transform.scale(pygame.image.load(weapon.image), (50, 50))
                    window.blit(icon, (x, y))
                    if pygame.Rect(x,y, slotSize, slotSize).collidepoint(mouseX, mouseY):
                        tooltipCandidate = weapon
                        tooltipPos = (x,y)
        if tooltipCandidate:
            self.drawToolTip(window, tooltipCandidate, *tooltipPos)

    def drawToolTip(self, window, obj, x, y):
        font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 18)
        lines = []
        if hasattr(obj, "name"):
            lines.append(f"Nazwa: {obj.name}")
        if hasattr(obj, "description"):
            lines.append(f"{obj.description}")
        if hasattr(obj, "damage"):
            lines.append(f"Obrażenia: {obj.damage}")
        if hasattr(obj, "range"):
            lines.append(f"Zasięg: {obj.range}")
        if hasattr(obj, "value"):
            lines.append(f"Wartość: {obj.value}g")
        width = max([font.size(line)[0] for line in lines]) + 10
        height = len(lines) * 20 + 10

        tooltipRect = pygame.Rect(x, y - height, width, height)
        pygame.draw.rect(window, (20,20,20), tooltipRect)
        pygame.draw.rect(window, (255, 255, 255), tooltipRect, 1)
        for i, line in enumerate(lines):
            surface = font.render(line, True, (255, 255, 255))
            window.blit(surface, (x+5, y-height + 5 + i * 20))