from gameCode.Classes.gameplay.InventoryItems.ItemClass import Item
from gameCode.Classes.gameplay.InventoryItems.items import PoisonAmulet

ITEM_CLASSES = {
    "Item" : Item,
    "PoisonAmulet": PoisonAmulet,
}

def createFromDict(data):
    itemClassName = data.get("itemClass") or data.get("item_class")
    print("⏳ Ładuję:", itemClassName)
    print("📦 ITEM_CLASSES:", list(ITEM_CLASSES.keys()))

    cls = ITEM_CLASSES.get(itemClassName)
    print("🔎 Otrzymana klasa:", cls)

    if cls is None:
        print(f"❌ Brak klasy '{itemClassName}' w ITEM_CLASSES")
        raise ValueError(f"Nieznana kategoria przedmiotu: {data}")

    if cls == Item:
        print("✅ Tworzę zwykły Item")
        return Item(
            name=data["name"],
            description=data["description"],
            value=data["value"],
            itemType=None,
            icon=data.get("icon"),
            usable=data.get("usable", True)
        )
    else:
        print("✅ Tworzę specjalny item:", cls)
        return cls()