class Human:
    def __init__(self,name = 'human_player'):
        self.name = name

    def update(self, enemy_action):
        human_decision = input('Please choose your decision. A for Attack, P for Prepare, D for Defend.')
        if human_decision == 'A':
            return 'Attack'
        elif human_decision == 'P':
            return 'Prepare'
        elif human_decision == 'D':
            return 'Defend'
