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
        return {
                "item_class": self.__class__.__name__,  # <--- KLUCZOWE
                "name": self.name,
                "description": self.description,
                "value": self.value,
                "type": self.itemType.name if self.itemType else None,
                "icon": self.icon,
                "usable": self.usable,
        }

