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

    def __init__(self, candidate1: Fighter, candidate2: Fighter):
        self.round = 0
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.round = 1
        self.winner = None
        self.candidate1.action = 'Prepare'
        self.candidate2.action = 'Prepare'
        self.commentator()
        return

    def congratulate(self):
        print('{} win the game!'.format(self.winner))

    def battle_loop(self):
        while not self.winner:
            self.round += 1
            self.candidate1.action_old = self.candidate1.action
            self.candidate2.action_old = self.candidate2.action
            self.candidate1.update(self.candidate2.action_old)
            self.candidate2.update(self.candidate1.action_old)
            self.commentator()
            if self.is_anyone_win():
                self.congratulate()

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
        elif self.candidate1.action == 'Prepare' and self.candidate2.action == 'Attack':
            self.winner = self.candidate2.name
            return True
        elif self.candidate2.action == 'Prepare' and self.candidate1.action == 'Attack':
            self.winner = self.candidate1.name
            return True
        elif self.round > 100:
            self.winner = 'NO BODY'
            return True
        return False


bot1 = Meower()
bot2 = Meower()
candidate1 = Fighter(bot1)
candidate2 = Fighter(bot2)
arena = Arena(candidate1, candidate2)
arena.battle_loop()
