class Fighter:
    def __init__(self, bot):
        fighter = bot()
        self.energy = 1
        self.action = 'Prepare'
        self.action_old = 'Prepare'
        self.strategy = fighter.update
        self.name = fighter.name

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

    def __init__(self, bot1, bot2):
        self.bot1 = bot1
        self.bot2 = bot2
        self.score = dict()
        candidate1 = Fighter(self.bot1)
        candidate2 = Fighter(self.bot2)
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.round = 1
        self.winner = None
        self.candidate1.action = 'Prepare'
        self.candidate2.action = 'Prepare'
        self.commentator()
        return

    def reinit(self):
        candidate1 = Fighter(self.bot1)
        candidate2 = Fighter(self.bot2)
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
        print('Round {}, {} decide to {:<7} while {} decide to {:<7}.'.format(self.round, self.candidate1.name,
                                                                              self.candidate1.action,
                                                                              self.candidate2.name,
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

    def multiple_rounds(self, rounds=1000):
        self.score['NO BODY'] = 0
        self.score[self.candidate1.name] = 0
        self.score[self.candidate2.name] = 0
        for _ in range(rounds):
            self.reinit()
            self.battle_loop()
            self.score[self.winner] += 1
        print('Final score {} to {}'.format(self.score[self.candidate1.name], self.score[self.candidate2.name]))
        if self.score[self.candidate1.name] > self.score[self.candidate2.name]:
            print('{} beat {} by {:.2%}!'.format(self.candidate1.name, self.candidate2.name, (
                    self.score[self.candidate1.name] - self.score[self.candidate2.name]) / rounds))
        elif self.score[self.candidate1.name] < self.score[self.candidate2.name]:
            print('{} beat {} by {:.2%}!'.format(self.candidate2.name, self.candidate1.name, (
                    self.score[self.candidate2.name] - self.score[self.candidate1.name]) / rounds))


'''以下为Arena使用范例'''
from bot_myc import *

arena = Arena(Meower, QLAgent)
arena.battle_loop()
arena.multiple_rounds(100000)
