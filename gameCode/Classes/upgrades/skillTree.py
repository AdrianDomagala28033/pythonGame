class SkillTree:
    def __init__(self, id, skillNodes):
        self.id = id
        self.nodes = {node.id: node for node in skillNodes}
        self.unlockedNodes = set()

    def canUnlock(self, nodeId, player):
        node = self.nodes[nodeId]
        if nodeId in self.unlockedNodes:
            return False
        for parentId in node.parentIds:
            if parentId not in self.unlockedNodes:
                return False
        return player.upgradePoints >= node.cost

    def unlock(self, nodeId, player):
        if self.canUnlock(nodeId, player):
            player.upgradePoints -= self.nodes[nodeId].cost
            self.unlockedNodes.add(nodeId)
            if self.nodes[nodeId].effect:
                self.nodes[nodeId].effect(player)
            return True
        return False
    def unlockToWeapon(self, nodeId, player, weapon):
        if self.canUnlock(nodeId, player):
            player.upgradePoints -= self.nodes[nodeId].cost
            self.unlockedNodes.add(nodeId)
            if self.nodes[nodeId].effect:
                self.nodes[nodeId].effect(weapon)
            return True
        return False