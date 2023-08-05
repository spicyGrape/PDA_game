# PDA game
*The game is called PDA (Prepare, Defend, Attack)*
## 规则
本游戏受启发于拍手游戏，在两名玩家之间以回合制进行。
### 能量
“能量”是游戏中的重要资源。每个玩家独享一定数量的能量，其初始值为0。若某位玩家的能量在某回合结束时小于0，则视为该玩家在该回合开始时就输掉了比赛。
### 动作
每个回合，每个玩家可以选择一个回合动作，所有玩家同时选择自己的回合动作，并可在做出选择后看见其他玩家选择的动作。回合动作可以改变玩家的能量数量。以下是全部可选动作：
1. Prepare：本回合结束时，本玩家能量+1。
2. Defend：本回合结束时，本玩家能量-1。
3. Attack：如果其他玩家的动作为Prepare，使其在本回合结束时输掉比赛。本回合结束时，本玩家能量-3。
## 代码要求
环境：Python 3.11
封装为单个类，允许文件附加权重。
该类需要对外开放两个方法：
1. 初始化函数：创建并初始化bot，无输入
2. 更新函数update()：更新bot状态，输入为上一回合其他玩家的动作（一个字符串），输出为本回合选择的动作（字符串）（Prepare，Defend，Attack）
可以使用numpy或者其他同层级的库，不可以使用任何基于numpy的库
3. 第一回合选取动作必须为Prepare, 因此从第二回合起，bot的update()才会被调用