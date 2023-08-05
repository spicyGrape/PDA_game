import random


class Arena:

    def __int__(self, candidate1, candidate2):
        self.round = 0
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.round = 1
        self.anyone_win = False
        self.action1 = 'Prepare'
        self.action2 = 'Prepare'
        return

    def battle_loop(self):

        while not self.anyone_win:
            self.round += 1

    def commentator(self):
        print('Round {}, candidate1 decide to {} while candidate2 decide to {}.'.format(self.round, self.action1, self.action2))


class Fighter:
    def __init__(self):
        self.energy = 0
        self.action = 'Prepare'



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
