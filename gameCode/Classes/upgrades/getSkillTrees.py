from gameCode.Classes.upgrades.skillNode import UpgradeNode
from gameCode.Classes.upgrades.skillTree import SkillTree


def getPlayerSkillTree():
    return SkillTree("player", [
        UpgradeNode(
            "strength_1",
            "Siła +1",
            "Zwiększa siłę",
            cost=1,
            effect=lambda p: (setattr(p, "strength", p.strength + 1))
        ),
        UpgradeNode("strength_2",
            "Siła +2",
            "Jeszcze większa siła",
            cost=1,
            effect=lambda p: setattr(p, "strength", p.strength + 2),
            parentIds=["strength_1"]),
        UpgradeNode("speed_1", "Szybkość +1", "Zwiększa prędkość", cost=1, effect=lambda p: setattr(p, "speed", p.speed + 1)),
        UpgradeNode("defense_1", "Obrona +1", "Zwiększa obronę", cost=1, effect=lambda p: setattr(p, "defense", p.defense + 1)),
    ])
def getBowSkillTree(bow):
    return SkillTree("bow", [
        UpgradeNode(
            id="bow_power_1",
            name="Obrażenia +2",
            description="Zwiększa obrażenia łuku",
            cost=1,
            effect=lambda bow: setattr(bow, "damage", bow.damage + 2)
        ),
        UpgradeNode(
            id="bow_speed_1",
            name="Szybsze strzały",
            description="Zmniejsza cooldown o 100ms",
            cost=1,
            effect=lambda _: setattr(bow, "cooldown",
                                     max(100, bow.cooldown - 100)),
            parentIds=["bow_power_1"]
        )
    ])
def getSwordSkillTree(sword):
    return SkillTree("sword", [
        UpgradeNode(
            id="sword_power_1",
            name="Obrażenia +5",
            description="Zwiększa obrażenia miecza",
            cost=1,
            effect=lambda sword: setattr(sword, "damage", sword.damage + 5)
        ),
        UpgradeNode(
            id="sword_range_1",
            name="Większy zasięg",
            description="Zwiększa zasięg o 20",
            cost=1,
            effect=lambda sword: setattr(sword, "range", sword.range + 20),
            parentIds=["sword_power_1"]
        )
    ])