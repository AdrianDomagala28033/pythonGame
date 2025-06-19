from gameCode.Classes.gameplay.effects.statusEffect import StatusEffect


def healEffect(target):
    healAmount = 30
    target.health = min(target.maxHealth, target.health + healAmount)
    print(f"Użyto mikstury, HP gracza: {target.health}/{target.maxHealth}")

def poisonEffect(target):
    target.health -= 0.02
    print(f"{target.tag} otrzymał 1 dmg od trucizny!")

def createPoisonEffect():
    return StatusEffect("Poison", duration=180, tickEffect=poisonEffect)