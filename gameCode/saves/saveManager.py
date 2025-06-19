import json
import os

from gameCode.Classes.gameplay.InventoryItems.ItemClass import Item
from gameCode.Classes.gameplay.InventoryItems.itemFactory import createFromDict
from gameCode.Classes.gameplay.InventoryItems.itemType import ItemType
from gameCode.Classes.gameplay.effects.effects import healEffect
from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.swordClass import Sword

saveFile = "savegame.json"
EFFECTS_MAP = {
    "healEffect": healEffect,
    None: None
}

# Mapa stringów na Enum typu
ITEM_TYPE_MAP = {
    "consumable": ItemType.CONSUMABLE,
    "key": ItemType.KEY,
    # dodaj inne typy, które masz w grze
}
def saveGame(gameData, filename="savegame.json"):
    with open(filename, "w") as f:
        json.dump(gameData, f, indent=4)
def loadGame(filename="savegame.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    # Odtwórz ekwipunek
    weaponInventory = [loadWeaponFromDict(w) for w in data.get("weaponInventory", [])]
    itemInventory = [createFromDict(i) for i in data.get("itemInventory", [])]

    return {
        "coins": data.get("coins", 0),
        "health": data.get("health", 100),
        "weaponInventory": weaponInventory,
        "itemInventory": itemInventory
    }
def deleteSave():
    if os.path.exists(saveFile):
        os.remove(saveFile)
def loadItemFromDict(data: dict):
    if data.get("category") == "item":
        itemType = ITEM_TYPE_MAP.get(data["type"], None)
        effect = EFFECTS_MAP.get(data.get("effect", None), None)

        return Item(
            name=data["name"],
            description=data["description"],
            value=data["value"],
            itemType=itemType,
            icon=data["icon"],
            effect=effect,
            usable=data["usable"]
        )
    elif data.get("tag") == "sword":
        # Zakładam, że masz klasę Weapon – jeśli nie, stwórz ją podobnie do Item

        return Sword(
            name=data["name"],
            damage=data["damage"],
            cooldown=data["cooldown"],
            direction=data["direction"],
            icon=data["icon"]
        )
    elif data.get("tag") == "bow":
        # Zakładam, że masz klasę Weapon – jeśli nie, stwórz ją podobnie do Item

        return Bow(
            name=data["name"],
            damage=data["damage"],
            cooldown=data["cooldown"],
            direction=data["direction"],
            icon=data["icon"]
        )
    else:
        raise ValueError(f"Nieznana kategoria przedmiotu: {data}")

def filterUsedKeys(itemList):
    return [
        item for item in itemList
        if item is not None and not (item.itemType == ItemType.KEY and not item.usable)
    ]
def loadWeaponFromDict(data: dict):
    tag = data.get("tag")
    if tag == "sword":
        return Sword(
                name=data["name"],
                damage=data["damage"],
                cooldown=data["cooldown"],
                direction=data["direction"],
                icon=data["icon"]
        )
    elif tag == "bow":
        return Bow(
                name=data["name"],
                damage=data["damage"],
                cooldown=data["cooldown"],
                direction=data["direction"],
                icon=data["icon"]
        )
    else:
        raise ValueError(f"Nieznany typ broni: {data}")