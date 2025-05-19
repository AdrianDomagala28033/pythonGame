import json
import os

from gameCode.Classes.UI.InventoryItems.Item import Item
from gameCode.Classes.UI.InventoryItems.itemType import ItemType
from gameCode.Classes.UI.InventoryItems.potions import healEffect
from gameCode.Classes.weapons.weapon import Weapon

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
    weaponInventory = [loadItemFromDict(w) for w in data.get("weaponInventory", [])]
    itemInventory = [loadItemFromDict(i) for i in data.get("itemInventory", [])]

    # Zwracamy wszystko
    return {
        "coins": data["coins"],
        "health": data["health"],
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
    elif data.get("category") == "weapon":
        # Zakładam, że masz klasę Weapon – jeśli nie, stwórz ją podobnie do Item

        return Weapon(
            name=data["name"],
            damage=data["damage"],
            image=data["image"],
            value=data["value"],
            range=data["range"]
        )
    else:
        raise ValueError(f"Nieznana kategoria przedmiotu: {data}")

def filterUsedKeys(itemList):
    return [
        item for item in itemList
        if item is not None and not (item.itemType == ItemType.KEY and not item.usable)
    ]