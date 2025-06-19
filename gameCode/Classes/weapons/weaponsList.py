import pygame.image

from gameCode.Classes.weapons.bowClass import Bow
from gameCode.Classes.weapons.swordClass import Sword

bows = [
    Bow("Basic Bow", 12, 500, 1, pygame.image.load("./images/weapons/standardBow.PNG")),
    Bow("Advanced Bow", 22, 500, 1, "./images/weapons/advancedBow.PNG"),
    Bow("Magic Bow", 15, 500, 1, "./images/weapons/magicBow.PNG"),
]

swords = [
    Sword("Basic Sword", 10, 100, 1, "./images/weapons/standardSword.PNG")
]