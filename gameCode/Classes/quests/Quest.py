class Quest:
    def __init__(self, name, description, goalType, target, requiredAmount, rewards=None):
        self.name = name
        self.description = description
        self.goalType = goalType
        self.target = target
        self.requiredAmount = requiredAmount
        self.progress = 0
        self.completed = False
        self.delivered = False
        self.rewardGiven = False
        self.rewards = rewards or {}

    @classmethod
    def fromDict(cls, data):
        return cls(
            name=data["name"],
            description=data["description"],
            goalType=data["goalType"],
            target=data["target"],
            requiredAmount=data["requiredAmount"]
        )

    def updateProgress(self, eventType, target):
        if self.completed:
            return
        if self.goalType == eventType and self.target == target:
            self.progress += 1
            if self.progress >= self.requiredAmount:
                self.completed = True

    def __str__(self):
        return f"{self.name}: {self.progress}/{self.requiredAmount} {'✅' if self.completed else ''}"
