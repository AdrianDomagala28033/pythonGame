import pygame

from gameCode.fonts.fonts import addFont


class CharacterMenu:
    def __init__(self, player, questManager, mapData):
        self.active = False
        self.player = player
        self.questManager = questManager
        self.mapData = mapData

        self.font = addFont("./fonts/Jacquard_24/Jacquard24-Regular.ttf", 28)

    def toggle(self, window):
        self.active = not self.active
        print(f"[CharacterMenu] Panel {'włączony' if self.active else 'wyłączony'}")
    def draw(self, window):

        if not self.active:
            return
        surface = pygame.Surface((700, 500))
        surface.fill((20, 20, 20))
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)

        # === Statystyki ===
        stats_y = 20
        stats = [
            f"Poziom: {self.player.level}",
            f"XP: {self.player.xp} / {self.player.xpToNextLevel}",
            f"HP: {self.player.health} / {self.player.maxHealth}",
            f"Monety: {self.player.coins}"
        ]
        for line in stats:
            text = self.font.render(line, True, (255, 255, 255))
            surface.blit(text, (20, stats_y))
            stats_y += 30

        # === Questy ===
        quest_y = 170
        questHeader = self.font.render("Aktywne zadania:", True, (255, 255, 0))
        surface.blit(questHeader, (20, quest_y))
        quest_y += 35

        for quest in self.questManager.getActiveQuests():
            status = "✓" if quest.completed else " "
            line = f"[{status}] {quest.name}"
            text = self.font.render(line, True, (255, 255, 255))
            surface.blit(text, (40, quest_y))
            quest_y += 30

            if hasattr(quest, 'progress') and hasattr(quest, 'requiredAmount'):
                progress = self.font.render(f"{quest.progress} / {quest.requiredAmount} ", True, (150, 150, 150))
                surface.blit(progress, (60, quest_y))
                quest_y += 25

            quest_y += 10

        window.blit(surface, (300, 100))