import json

from gameCode.Classes.quests.Quest import Quest


def loadQuestsFromFile(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        quests = []
        for q in data:
            quest = Quest(
                q["name"],
                q["description"],
                q["goalType"],
                q["target"],
                q["requiredAmount"],
                rewards=q.get("rewards", {})
            )
            quests.append(quest)
        return quests