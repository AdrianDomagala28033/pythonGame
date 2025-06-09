class QuestManager:
    def __init__(self):
        self.quests = []
    def addQuest(self, quest):
        if quest not in self.quests:
            self.quests.append(quest)
            print("➕ Dodano do questManager:", quest.name)
        else:
            print("⚠️ Quest już istnieje:", quest.name)

    def updateQuests(self, eventType, target):
        for q in self.quests:
            q.updateProgress(eventType, target)

    def getActiveQuests(self):
        return [q for q in self.quests if not q.completed]

    def getAllQuests(self):
        return self.quests