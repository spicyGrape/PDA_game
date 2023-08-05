import random
from bot_myc import *


class Fighter:
    def __init__(self, bot):
        self.energy = 0
        self.action = 'Prepare'
        self.action_old = 'Prepare'
        self.strategy = bot.update
        self.name = bot.name

    def prepare(self):
        self.energy += 1

    def attack(self):
        self.energy -= 3

    def defend(self):
        self.energy -= 1

    def update(self, enemy_action_old: str) -> str:
        self.action = self.strategy(enemy_action_old)
        if self.action == 'Prepare':
            self.prepare()
        elif self.action == "Attack":
            self.attack()
        elif self.action == 'Defend':
            self.defend()
        return self.action


class Arena:

    def __int__(self, candidate1: Fighter, candidate2: Fighter):
        self.round = 0
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.round = 1
        self.winner = ''
        self.candidate1.action = 'Prepare'
        self.candidate2.action = 'Prepare'
        return

    def battle_loop(self):
        while not self.winner:
            self.round += 1
            self.candidate1.action_old = self.candidate1.action
            self.candidate2.action_old = self.candidate2.action
            self.candidate1.update(self.candidate2.action_old)
            self.candidate2.update(self.candidate1.action_old)

    def commentator(self):
        print('Round {}, candidate1 decide to {} while candidate2 decide to {}.'.format(self.round,
                                                                                        self.candidate1.action,
                                                                                        self.candidate2.action))

    def is_anyone_win(self) -> bool:
        if self.candidate1.energy < 0:
            self.winner = self.candidate2.name
            return True
        elif self.candidate2.energy < 0:
            self.winner = self.candidate1.name
            return True