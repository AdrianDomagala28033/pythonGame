class Item:
    def __init__(self, name, description, value, itemType, icon=None, effect=None, usable = True):
        self.name = name
        self.description = description
        self.value = value
        self.itemType = itemType
        self.icon = icon
        self.effect = effect
        self.usable = usable

    def use(self, player):
        if self.usable:
            if self.effect:
                self.effect(player)
        else:
            print(self.name)

