import pygame

class Physic:
    def __init__(self, verVelocity, horVelocity, acc, maxVelocity):
        self.verVelocity = verVelocity
        self.horVelocity = horVelocity
        self.acc = acc
        self.maxVelocity = maxVelocity
    def physicTick(self):
        self.verVelocity -= 0.3