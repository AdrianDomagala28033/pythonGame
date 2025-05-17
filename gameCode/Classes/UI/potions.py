from gameCode.Classes.UI.Item import Item
from gameCode.Classes.UI.itemType import ItemType

def heal_effect(player):
    healAmount = 30
    player.health = min(player.maxHealth, player.health + healAmount)
    print(f"Użyto mikstury, HP gracza: {player.health}/{player.maxHealth}")

health_potion = Item(
    name="Mikstura Zdrowia",
    description="Przywraca 30 punktów zdrowia.",
    value=10,
    itemType=ItemType.CONSUMABLE,
    icon="./images/healthPotion.PNG",
    effect=heal_effect
)