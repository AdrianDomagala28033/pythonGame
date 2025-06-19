from gameCode.Classes.gameplay.InventoryItems.ItemClass import Item
from gameCode.Classes.gameplay.InventoryItems.itemType import ItemType
from gameCode.Classes.gameplay.effects.effects import healEffect

health_potion = Item(
    name="Mikstura Zdrowia",
    description="Przywraca 30 punktów zdrowia.",
    value=10,
    itemType=ItemType.CONSUMABLE,
    icon="./images/healthPotion.PNG",
    effect=healEffect
)