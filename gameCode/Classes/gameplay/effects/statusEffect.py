class StatusEffect:
    def __init__(self, name, duration, tickEffect, image=None):
        self.name = name
        self.duration = duration
        self.tickEffect = tickEffect
        self.image = image

    def apply(self, target):
        self.tickEffect(target)
        self.duration -= 1
        return self.duration > 0