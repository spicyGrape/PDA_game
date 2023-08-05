import random
class Meower:

    def __init__(self):
        self.agentEnergy = 0
        self.name = 'SillyB'

    def update(self, act: str) -> str:
        if self.agentEnergy >= 3:
            temp = random.random()
            if temp > 0.6:
                self.agentEnergy -= 3
                return "Attack"
            elif temp > 0.2:
                self.agentEnergy -= 1
                return "Defend"
            else:
                self.agentEnergy += 1
                return "Prepare"
        elif self.agentEnergy >= 1:
            temp = random.random()
            if temp > 0.6:
                self.agentEnergy -= 1
                return "Defend"
            else:
                self.agentEnergy += 1
                return "Prepare"
        else:
            self.agentEnergy += 1
            return "Prepare"
