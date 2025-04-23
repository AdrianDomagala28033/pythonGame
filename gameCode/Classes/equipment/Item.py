class Item:
    def __init__(self, name, description, value, itemType, icon=None, effect=None):
        self.name = name
        self.description = description
        self.value = value
        self.itemType = itemType
        self.icon = icon
        self.effect = effect

    def use(self, player):
        if self.effect:
            self.effect(player)

