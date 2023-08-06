import random
import json


class QLAgent:
    RTable = {
        ("Prepare", "Prepare"): -0.05,
        ("Prepare", "Defend"): -0.05,
        ("Prepare", "Attack"): -1,

        ("Defend", "Prepare"): -0.1,
        ("Defend", "Defend"): 0,
        ("Defend", "Attack"): 0.1,

        ("Attack", "Prepare"): 1,
        ("Attack", "Defend"): -0.2,
        ("Attack", "Attack"): -0.1,
    }
    alpha = 0.1
    gamma = 0.9
    epsilon = 0.2
    '''
    key:(agentAction,enemyAction)
    value:reward
    '''

    def __init__(self, name="Shitting Lee", path="./agent.json") -> None:
        self.name = name
        self.agentAction = "Prepare"
        self.enemyAction = "Prepare"
        self.agentEnergy = 1
        self.enemyEnergy = 1

        self.QTable = {}
        '''
        key:Encoded
        value:{
            key:action
            value:Q
        }
        '''
        try:
            with open(path, 'r') as f:
                self.QTable = json.load(f)
        except:
            pass

    def __clear(self) -> None:
        self.agentAction = "Prepare"
        self.enemyAction = "Prepare"
        self.agentEnergy = 1
        self.enemyEnergy = 0

    def __state(self) -> str:
        return str(self.agentEnergy) + '_' + str(self.enemyEnergy)

    def __default_policy(self, act: str) -> str:
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

    def __action_space(self) -> tuple:
        if self.agentEnergy >= 3:
            return "Attack", "Defend", "Prepare"
        elif self.agentEnergy >= 1:
            return ("Defend", "Prepare")
        else:
            return ("Prepare",)

    def __energy_delta(self, act: str) -> int:
        match act:
            case "Prepare":
                return 1
            case "Defend":
                return -1
            case "Attack":
                return -3

    def __next_state(self, agentCurAct, enemyCurAct) -> str:
        match agentCurAct:
            case "Prepare":
                nextAgentEnergy = self.agentEnergy + 1
            case "Defend":
                nextAgentEnergy = self.agentEnergy - 1
            case "Attack":
                nextAgentEnergy = self.agentEnergy - 3
        match enemyCurAct:
            case "Prepare":
                nextEnemyEnergy = self.enemyEnergy + 1
            case "Defend":
                nextEnemyEnergy = self.enemyEnergy - 1
            case "Attack":
                nextEnemyEnergy = self.enemyEnergy - 3
        return str(nextAgentEnergy) + "_" + str(nextEnemyEnergy)

    def update(self, act: str) -> str:
        self.enemyAction = act
        self.enemyEnergy += self.__energy_delta(act)

        q = {}
        s = self.__state()
        if s in self.QTable:
            q = self.QTable[s]
        if len(q) > 0:
            agentAction = max(q)
        else:
            agentAction = self.__default_policy(act)

        self.agentEnergy += self.__energy_delta(act)

        return agentAction

    def train(self, enemyCurAct: str) -> None:
        """
        输入：
            训练用bot(垫脚石)**本回合**将会采取的行动
        """

        # ε-greedy
        q = {}
        s = self.__state()
        action_space = self.__action_space()
        if s in self.QTable:
            q = self.QTable[s]

        if random.random() > self.epsilon and len(q) > 0:
            # greedy
            agentCurAct = max(q, q.get)
        else:
            # explore
            agentCurAct = random.choice(action_space)

        self.agentEnergy += self.__energy_delta(agentCurAct)
        self.enemyEnergy += self.__energy_delta(enemyCurAct)

        s_ = self.__state()

        # update QTable
        r = self.RTable[(agentCurAct, enemyCurAct)]
        if len(q) == 0:
            self.QTable[s] = {}
        match r:
            case -1:
                self.QTable[s][agentCurAct] = -1
                self.__clear()
            case 1:
                self.QTable[s][agentCurAct] = 1
                self.__clear()
            case _:
                if agentCurAct in self.QTable[s]:
                    q_s_a = self.QTable[s][agentCurAct]
                else:
                    q_s_a = 0

                q_ = self.QTable[s_]
                if len(q_) == 0:
                    self.QTable[s_] = {}
                    q_s_a_ = 0
                else:
                    q_s_a_ = q_[max(q_)]

                self.QTable[s][agentCurAct] = q_s_a + \
                                              self.alpha * (r + self.gamma * q_s_a_ - q_s_a)
        return

    def output(self, path="./agent.json") -> None:
        with open(path, 'w+') as f:
            json.dump(self.QTable, f)


class Meower:
    def __init__(self, name="Silly Meow") -> None:
        self.agentEnergy = 1

        self.name = name

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


if __name__ == "__main__":
    pass
    """
    这是一个笨蛋级的东西
    在训练过程中,甚至假定对手只会以某种固定(而非概率性)的策略行动
    
    设计的训练方法:
    1.创建QLAgent对象A
    2.创建一个拥有已知,确定策略的对象B
    3.进行epsilon次训练,将B.update()传给A.train()进行训练
    4.训练完成后,用A.output()输出训练得到的权重
    注意:
    请自己debug
    权重路径请自行考虑
    """
