import random


class Arena:

    def __int__(self, candidate1, candidate2):
        self.round = 0
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.round = 0
        self.anyone_win = False
        return

    def battle_loop(self):

        while not self.anyone_win:
            self.round += 1



class Meower:
    """"毛奕澄的BOT"""

    def __init__(self):
        self.agentEnergy = 0

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
