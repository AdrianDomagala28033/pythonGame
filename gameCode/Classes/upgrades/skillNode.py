class UpgradeNode:
    def __init__(self, id, name, description, cost=1, effect=None, parentIds=None):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.effect = effect
        self.unlocked = False
        self.parentIds = parentIds or []

    def unlock(self, player):
        if not self.unlocked and player.upgradePoints >= self.cost:
            player.upgradePoints -= self.cost
            if self.effect:
                self.effect(player)
            self.unlocked = True
