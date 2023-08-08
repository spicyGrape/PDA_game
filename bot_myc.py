import random
import json
from tqdm import tqdm


def arg_max(dic: dict) -> str:
    return max(zip(dic.values(), dic.keys()))[1]


class QLAgent:
    RTable = {
        ("Prepare", "Prepare"): 0.00,
        ("Prepare", "Defend"): 0.00,
        ("Prepare", "Attack"): -1,

        ("Defend", "Prepare"): -0.01,
        ("Defend", "Defend"): 0.00,
        ("Defend", "Attack"): 0.02,

        ("Attack", "Prepare"): 1,
        ("Attack", "Defend"): -0.01,
        ("Attack", "Attack"): 0.01,
    }
    '''
    key:(agentAction,enemyAction)
    value:reward
    '''
    alpha = 0.01
    gamma = 0.9
    epsilon = 0.5

    def __init__(self, name="Shitting Lee", path="./agent.json", mode="play") -> None:
        self.name = name
        self.agentEnergy = 1
        match mode:
            case "play":
                self.enemyEnergy = 0
            case "train":
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
        self.agentEnergy = 1
        self.enemyEnergy = 1

    def reset(self) -> None:
        self.agentEnergy = 1
        self.enemyEnergy = 0

    def __state(self) -> str:
        return str(self.agentEnergy) + '_' + str(self.enemyEnergy)

    def __default_policy(self, act: str) -> str:
        if self.agentEnergy >= 3:
            temp = random.random()
            if temp > 0.6:
                return "Attack"
            elif temp > 0.2:
                return "Defend"
            else:
                return "Prepare"
        elif self.agentEnergy >= 1:
            temp = random.random()
            if temp > 0.6:
                return "Defend"
            else:
                return "Prepare"
        else:
            return "Prepare"

    def __action_space(self) -> tuple:
        if self.agentEnergy >= 3:
            return "Attack", "Defend", "Prepare"
        elif self.agentEnergy >= 1:
            return "Defend", "Prepare"
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

    def update(self, act: str) -> str:
        self.enemyEnergy += self.__energy_delta(act)

        q = {}
        s = self.__state()
        if s in self.QTable:
            q = self.QTable[s]
            # print(q)
        if len(q) > 0:
            agentAction = arg_max(q)
            if q[agentAction] == -1:
                agentAction = self.__default_policy(act)
        else:
            agentAction = self.__default_policy(act)

        self.agentEnergy += self.__energy_delta(agentAction)

        return agentAction

    def train(self, enemyCurAct: str) -> (str, bool):
        """
        输入：
            训练用bot(垫脚石)**本回合**将会采取的行动
        输出:
            agent本回合输出
            True重置
        """

        # ε-greedy
        q = {}
        s = self.__state()
        action_space = self.__action_space()

        if s in self.QTable:
            q = self.QTable[s]

        if random.random() > self.epsilon and len(q) > 0:
            # greedy
            agentCurAct = arg_max(q)
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
                ends = True
            case 1:
                self.QTable[s][agentCurAct] = 1
                self.__clear()
                ends = True
            case _:
                ends = False
                if agentCurAct in self.QTable[s]:
                    q_s_a = self.QTable[s][agentCurAct]
                else:
                    q_s_a = 0

                if not s_ in self.QTable:
                    self.QTable[s_] = {}
                q_ = self.QTable[s_]
                if len(q_) == 0:
                    self.QTable[s_] = {}
                    q_s_a_ = 0
                else:
                    q_s_a_ = q_[max(q_)]

                self.QTable[s][agentCurAct] = q_s_a + \
                                              self.alpha * (r + self.gamma * q_s_a_ - q_s_a)
        return agentCurAct, ends

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


episode = 10000000

if __name__ == "__main__":
    """
    这是一个笨蛋级的东西
    在训练过程中,甚至假定对手只会以某种固定(而非概率性)的策略行动

    设计的训练方法:
    1.创建QLAgent对象A
    2.创建一个拥有已知,确定策略的对象B
    3.进行episode次训练,将B.update()传给A.train()进行训练
    4.训练完成后,用A.output()输出训练得到的权重
    注意:
    请自己debug
    权重路径请自行考虑
    """
    learner = QLAgent("learner", "./agent.json", "train")
    shitter = QLAgent("shitter")
    # train
    learnerAction = "Prepare"
    shitterAction = "None"
    for i in tqdm(range(episode)):
        shitterAction = shitter.update(learnerAction)
        learnerAction, ends = learner.train(shitterAction)
        if ends:
            shitter.reset()
            learnerAction = "Prepare"
            shitterAction = "None"

    learner.output()
