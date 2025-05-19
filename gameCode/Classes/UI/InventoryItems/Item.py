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
    def toDict(self):
        return dict(category="item",
                    name = self.name,
                    description= self.description,
                    value=self.value,
                    type=self.itemType.name if self.itemType else None,
                    icon=self.icon,
                    effect=self.effect.__name__ if self.effect else None,
                    usable=self.usable)

