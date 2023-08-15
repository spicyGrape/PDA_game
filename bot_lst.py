import json


class Participant:
    def __init__(self):
        self.energy = 0

    def energy_update(self, action: str):
        if action == 'Prepare':
            self.energy += 1
        elif action == 'Defend':
            self.energy -= 1
        elif action == 'Attack':
            self.energy -= 3


class CleverMeow:
    def __init__(self, name='clever Meow', path='./clever_meow_magic_scroll.json', policy_number=0):
        self.clever_meow = Participant()
        self.clever_meow.energy_update('Prepare')
        self.enemy = Participant()
        self.magic_scroll = open(path, 'r')
        self.policy_group = json.load(self.magic_scroll)
        self.policy = self.policy_group[policy_number]

    def update(self, enemy_action: str):
        self.enemy.energy_update(enemy_action)

    def think(self) -> list:
        idea = [self.clever_meow.energy * x + self.enemy.energy * y for x, y in (self.policy[0], self.policy[1])]
        
        pass
