from gameCode.Classes.gameplay.InventoryItems.itemType import ItemType


class Weapon:
    def __init__(self, name, damage, image, value, range):
        self.name = name
        self.damage = damage
        self.range = range
        self.image = image
        self.value = value
        self.type = ItemType.WEAPON
        self.tag = ""
    def toDict(self):
            return dict(category="weapon", name = self.name, damage = self.damage, range = self.range, image=self.image, value=self.value, tag=self.tag)
    def getEffectiveDamage(self, playerLevel):
        return self.damage + int(playerLevel * 0.5)

    def applyUpgrade(self, upgradeId):
        print(f"🔥 Upgrade {upgradeId} applied to {self.name}")
        if upgradeId == "bow_power_1":
            self.damage += 5
        elif upgradeId == "bow_speed_1":
            self.cooldown = max(100, self.cooldown - 100)