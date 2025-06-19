from gameCode.Classes.gameplay.InventoryItems.ItemClass import Item
from gameCode.Classes.gameplay.InventoryItems.itemType import ItemType
from gameCode.Classes.gameplay.effects.effects import createPoisonEffect


class PoisonAmulet(Item):
    def __init__(self):
        super().__init__(
            name="Amulet trucizny",
            description="Każdy atak zatruwa przeciwnika",
            value=200,
            itemType=ItemType.ACCESSORY,
            icon="./images/playerAnimation/walkingCharacter.png",
            usable=False
        )
        self.passiveEffect = createPoisonEffect