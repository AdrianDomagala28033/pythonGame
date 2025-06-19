import pygame


class BaseNpcPanel:
    def __init__(self, npc, player):
        self.npc = npc
        self.player = player
        self.active = False
        self.npc.dialogOpen = False

    def toggle(self):
        self.active = not self.active
        if not self.active:
            self.npc.dialogOpen = False  # domykamy również NPC logicznie
        else:
            self.npc.dialogOpen = True

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle()

    def draw(self, surface):
        raise NotImplementedError("draw() musi być zaimplementowane w klasie dziedziczącej")

    def toggle(self):
        self.active = not self.active
        self.npc.dialogOpen = self.active
        print(f"🔁 toggle panel — active: {self.active}")