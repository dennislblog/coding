---
title: 控制问题
date: 2021-03-17
autoGroup-4: 强化学习
tags:
  - Knowledge
sidebarDepth: 3
---


::: tip
在这里记录强化学习知识
:::

<!-- more -->

<style>
blockquote > p {
    text-indent: 25px;
}
blockquote > p:first-child{
    text-indent: 0px;
}
</style>


[ Katex Support ](https://katex.org/docs/supported.html)

## 最优控制

::: warning introduction 
1. 假定环境完全已知情况下解MDP, $P$和$R$都是给定不需要估计, 解最优决策
2. 真正的强化学习问题还涉及产生服从环境分布的数据, 这里直接假定我们不仅获得了数据, 而且直接得到了环境动态转换规律

> **价值的思想**： 每一个状态都与最终获得的奖励存在某个概率上的联结, 所以这些状态是具有价值的, 而且注意某些状态的价值获得是建立在`之后我们的每一步都是最优`的条件上获得的(包括初始状态). ==只有走法正确, 才能兑现价值==

> **基于价值的思路**： 有点像是`backtrack`, 从后往前推, 先找到确定能获得奖励的状态, 对于中间状态, 考虑各种动作使其能够到达这些"必胜状态"(V=1)或者"必平状态"(V=0). 我们先是算出了一些状态的价值, 再用这些已知的价值去计算别的状态的价值, 直到将所有状态的价值都算出来. $V(s) = \max_a \sum_{s'}V(s')P_{s,s'}^a$, 其中由于从$t= T \rightarrow 1$来推, $V(s')$都是已知的(但可以继续被更新)

> ![马尔科夫-small](~@assets/rl_control-01.png#right)
> **为什么马尔科夫性质如此重要**： 上面要计算每一个状态的价值, 我们需要枚举所有此刻从该状态出发到终点的所有可能路径, 这显然计算量太过庞大. 但如果我们假设==总体的"最大"意味着每个部分也"最大"==, 即如果$t_1 \rightarrow t_2$的最优路径$\color{red} \tau_1$确定了, $t_2 \rightarrow t_3$的路径选择就都是基于$\color{red} \tau_1$, 但是如果马尔科夫不满足(例如厚积薄发这种东西), 则我们必须枚举所有$t_1 \rightarrow t_3$的路径, 因为$\color{blue} \tau_2$也许在$s_1 \rightarrow s_2$段不如$\color{red} \tau_1$, 但厚积薄发了. 
> 相反如果MDP满足马尔科夫, 则这两条路径在$t_2$之后发生的一切都只和$s_2$有关, 所以理论上$\color{blue} \tau_2$永远不可能比$\color{red} \tau_1$要好(我之后跟着你走!)

**思考**: 是不是最好把状态定义为不能重复访问, 比如围棋里面一旦下了某一个子, 在不能悔棋的情况下再也回不到这个状态了, 这样才能保证backward deduction先把离终态近的先求出来
:::

## 动态规划

::: tip introduction
### 策略迭代

> ![策略迭代-small](~@assets/rl_control-02.png#right)
> 假设$P_{s,s'}^a \in \mathbb{R}^{5\times 3\times 5}, R_s^a \in \mathbb{R}^{5\times 3}$, 假设效用随时间衰减$(\gamma)$, 假设这个游戏永远不结束, 我们没法`backtrack`, 从终态往前推
> 
> **策略评估**： 假设我们现在有一个策略$\pi \in \mathbb{R}^{5 \times 1}$, 记录着每一个状态$s_1,\cdots, s_5$分别对应的决策$a$, 这时我们用$V_\pi (s) = R + \gamma \sum_{s'}P V_\pi(s')$分别作用于$5$个状态, 得到$5$个线性方程组, 对应5个未知量$V_\pi(s_i)$, 这样就得到了在特定策略下, 所有状态的价值(状态是穷尽, 但时间是无穷的).

> 对于拥有$5$个不同状态, $3$个不同动作的MDP而言, 穷举$3^5 = 243$种不同的策略$\pi$, 对每一种策略都做一次`策略评估`, 然后检查每一个状态下$243$个$V_\pi (s)$, 就得到了最优策略. 但是如果状态数量与动作数量比较多, 则枚举法计算量太大(untractable?). 要解决$n$阶线性方程组需要$O(n^3)$复杂度, 为了降低计算复杂度, 用迭代数值解法简化运算

> **Jacobi Method**: 求解$x = Ax + b$线性方程组, 令$x_{i+1} = Ax_i + b$直到$x_i$与$x_{i+1}$的距离很小为止. 由于在MDP中, $P(s,a,s')$的行之和始终等于$1$(状态和动作确定的情况下, 到达所有可能的下个状态的概率之和等于$1$), $\mathbf{I} - \gamma P$满足==严格对角优势==, 所以策略会收敛! 此外计算复杂度为$O(n^2\cdot k), \; k \leq n$, 其中$k$为迭代次数
> ```
> 雅阁比迭代->策略评估
> for j = 1, 2, ..., k do: //continue until V(s) doesn't change much
>          a = pi(s)
>       V(s) = R(s,a) + r Sum[P(s,a,s')V(s') for all s']  //x = b + A x
> ```

与基础版的**策略迭代**相比, 这种迭代法不要求价值函数$V_\pi(s)$估计准确(而且策略差的时候价值估计准确重要吗?), 关键**策略提升**并不是严格比较$V_\pi(s)$, 而是找出$a = \argmax_a(R(s,a) + \gamma \sum_{s'} P(s,a,s') V_\pi(s))$重要. 另一个是可以把上一次**策略评估**的解$x_i = V_\pi$作为下一次**策略评估**的初始解, 从而重复使用了上次Jacobi迭代的计算结果

> **策略提升**: 用算出来的$V_\pi(s)$去改进当前策略$\pi$, 新策略$\pi_{i+1}(s) = \argmax_a[R + \gamma \sum_{s'}P(s,a,s')V_{\color{blue} \pi}(s)]$. 以当前的做题水平, 每道题都尽力去答, 能更掌握答题技巧? 策略提升的数学证明待定! 而且策略是否能够收敛? 
> ```
> 策略提升
> pi'(s) = argmax_a R(s,a) + r Sum[P(s,a,s')V(s') for all s'] 
> ```

所以策略迭代就是循环使用： 1) **策略评估**计算每一个状态的策略-价值; 2) **策略提升**来改进当前的策略. 

### 值迭代
在策略迭代里, 价值的估计只是辅佐算法得到"最佳策略", 而值迭代的目的则是去拟合MDP真正的value table. 考虑`Jacobi Method`用来节省计算量到最极端的情况(牺牲精确度, 换取计算量), $k=1$, 每次价值表只更新一步, 那么可以把**策略评估**和**策略提升**合并为一个步骤
> ```
> 值迭代
> for j = 1, 2, ..., k do: //continue until V(s) doesn't change much
>     V(s) = max_a R(s,a) + r Sum[P(s,a,s')V(s') for all s']  // x = max(b + Ax)
> ```
整个过程里并不涉及**策略提升**, 而是假定价值表的提升能够帮助我们得到一个更好的策略? 但由于加入了`max`这个操作符号, 使得原本的线性方程组变成了非线性(折一下!), 即使线性方程组$Ax + b = 0$在non-singular A的条件下有唯一解(==n个线性无关的超平面交于一点==), 但如果加入了`max operator`, $\max(Ax+b, Cx+d) =0$很可能没有唯一解==(n个折了一下的超平面很可能交于不止一点)==, 但由于贝尔曼方程很特殊(==P矩阵每一行都是$1$, 衰减也是在0~1之间==), 所以它是有唯一解的(证明待定)

<!-- 总结： 两种方法的算力瓶颈都是$O(mn^2)$, $n$为状态数量, $m$为动作数量 -->

### 软提升
**策略提升**中, 新策略的选择是基于假设：如果按照当前策略$\pi$走一步$a$, 且继续按照$\pi$操作, 所能获得的最大收益. 但是策略由$\pi \rightarrow \pi'$之后, "后续就不是按照原策略走了", 所以策略提升未必让策略变得更好. 一个很自然的想法是能不能不要激进地更新$\pi$ (小步慢走)

传统上认为策略应该是确定性的: 即某个状态下应该存在一个最好的决策, 但相比随机性策略这样做有两点不好： 1) 前后策略可能相差迥异(比如我那个contract problem直接得到最优解), 每次$\argmax$都要重新求解; 2) 神经网络等复杂模型输出概率比输出$0,1$, 梯度会更加柔和一些? 

相应的, 在值迭代里, 策略是隐藏在价值表中的, 为了让策略更新不那么激进, 我们希望价值表的更新也不要那么激进(有点像梯度更新, 价值就是策略的梯度?), 我们可以把修改后的策略和价值迭代算法总结如下

> ```
> 策略迭代
> for i = 1, 2, ..., N do:      //continue until pi(s) doesn't change much
>     for j = 1, 2, ..., K do:  //原来是 a 直接等于 pi(s), 确定性策略
>         V(s) = Sum{ pi(a|s) (R(s,a) + r Sum[P(s,a,s')V(s') for all s']) for all a}
>     pi'(a|s) = normalize{ R(s,a) + r Sum[P(s,a,s')V(s') for all s'] }
>     
> 价值迭代
> for i = 1, 2, ..., N do:      //continue until V(s) doesn't change much
>     V'(s) = V(s) + alpha { max_a R(s,a) + r Sum[P(s,a,s')V(s') for all s'] - V(s) }  //alpha is the learning rate
> ```
> 值迭代不需要用到创建的策略表, 直接用给定的$P, R$即可, 当$P, R$需要被估计的时候, 就需要用到这两类算法的变式： DQN与PG. 比如对于DQN而言, 可以用任何时候从环境交互那里得到的数据来估计更好的值函数, 但对于PG而言, 则只能用当前策略与环境产生的数据来训练当前的策略网络. 
> ![算法比较-small](~@assets/rl_control-03.png#center)
:::

## 连续动作和状态

::: warning introduction
状态和动作都是连续的MDP如何表达? $P(s,a,s')$用一个复杂的概率分布表示, 假设环境是deterinistic and time consistent (确定性且时齐), i.e., $s' = f(s,a)$, 同理奖励也是确定和时齐, i.e., $r = g(s,a)$. 

> **Linear Quadratic Regulator**: 假定最简单的线性函数, $f(s,a) = As +Ba$, 奖励函数如果也是线性的话, 优化目标就不会有最大值, 因此我们用正定二次函数来表示$g(s,a)$, 这种状态转移关系是线性, 损失函数是二次函数的问题, 我们称其为LQR
> | 初始状态   | $x_0$ | 
> |  :----  | :----  | 
> | 状态转移关系 | $x' = Ax + Bu$ | 
> | 目标 | 最小化$J = \sum_{t=0}^T (x^T Q x + u^T R u)$ |
> 对于怎么解这个`sequential quadratic programing`, 我在合同问题里已经演示了, 对于确定系数的正定二次目标函数$J$, 总是存在最优控制$u_1, \cdots, u_T$使得$J$最小(一阶导数为0).
> 
> 但是如果不能通过线性代数简化关系, 按传统求导的方式, 假设控制$u_i$是$k$维, 则${\bf u}$是$kT$维的, 解整个线性方程组(还只是得到$u$关于$x$的表达式)就需要$O((kT)^3)$, 所以对于时间长, 控制多的问题而言, 直接通过展开$J$求解, 不现实. 既然这种通过直接求策略(控制)的方法计算过于复杂, 我们能不能借用动态规划的思想, ==将大的问题分拆成小的问题, 先解决小的问题, 再利用小问题的解去解大的问题==, 
> 

### LQR控制器
> 假设我们要解这样一个问题
> $$\begin{aligned}
>    \min \; & \sum_{t=0}^{100} (x^T_t Q x_t + u^T_t R u_t) \\
>    s.t. \; & x_{t+1} = A x_t + B u_t \; x_0 = a 
> \end{aligned}$$

要注意的是我们面对的是非时齐MDP, 不同时间下每个状态的价值会有变化, 或者说现在进行到第几回合是一件重要的事情. 因此我们有一个**状态-时间价值函数**$V(x,t)$, 表示我们在$t$时刻的$x$状态下, 如果后续都按照最优策略走, 能获得的最大收益/最小损失. 

> 首先考虑$t=100$, 对$u_{100}$求导, 由于$x_{100}$是已知的, 一阶导数为$0\Rightarrow u_{100} = 0$
> 
> 接下来考虑$t=99$, $x_{99}$已经发生了, $u_{99}$这个行为会产生两部分损失: 1) 直接损失; 2) $t=100$还未发生的损失, 我们引入一个新的$Q$函数来记录这个损失, $Q(x,u,t)$, 一个关于状态, 控制与实践的状态-动作函数, 表示我们在$t$时刻的$x$状态下, 如果采取$u$这个行为,  如果后续都按照最优策略走, 能获得的最大收益/最小损失.由于$x_{100}$可以用$f(x_{99}, u_{99})$表示, 并且$u_{100} = 0$, 于是我们得到
> $$\begin{aligned}
>   Q(x,u,99) &= x^TQx + u^TRu + V(Ax+Bu,100) \\
>             &= x^TQx + u^TRu + (Ax+Bu)^TQ(Ax+bu)
> \end{aligned}$$
> 一阶导数为$0\Rightarrow u_{99} = K_{99} x_{99}$, 我们可以进而得到$V(x,99) = \min_u Q(x,u,t)$
> 
> 接下来考虑$t=98$, 同样两部分损失：即时$\color{red} x_{98}^TQx_{98}+ u^T_{98}Ru_{98}$和将来$\color{blue} V(x,99)$, 之前我们已经把$V(x,99)$求出来了, 加上状态转移方程$x_{99} = Ax_{98} + Bu_{98}$, 由于$x_{98}$已经确定, 最后$V(x,98)$是一个只含有$u_{98}$的二次函数, 一阶导数为$0\Rightarrow u_{98} = K_{98} x_{98}$, 公式过于复杂, 但是有具体数值就很好解, 这一步得到$u_{98}$和$V(x,98)$, 后者在$t=97$中被使用
> 
> 不断重复上面过程, 由于LQR的状态转移是线性, 惩罚函数是二次的, 因此任何一个时刻$t$, 最佳控制都是一个关于状态的线性表达式$u_t = K_t x_t$, 状态价值->状态动作函数都是关于控制变量的正定二次函数$u_t = \argmin_u u^T_t Q u_t$, 直到$t=0$, 这样我们就得到了$u_0$, 然后`backward recursion`就结束了
> 
> 接下来根据$x_0$和$u_0$以及状态转移方程$x' = f(x,u)$做`forward recursion`, 使用`backward recursion`中保存的中间变量$K_t$以及$Q(x,u,t), V(x,t)$的系数, 依次计算出$x_1, u_1=K_1x_1, x_2, u_2=K_2x_2,\cdots, x_T,u_T$, 总结如下
> ```
> backward recursion
> for t = T, T-1, ..., 0 do:
>     Q(x,u,t) = C(x,u) + V(f(x,u), t+1)
>          u_t = argmin_u Q(x_t,u,t) = K_t x_t + k_t
>       V(x,t) = min_u Q(x,u,t)
> 
> forward recursion
> for t = 0, 1, ..., T do:
>          u_t = K_t x_t + k_t
>          x_t = f(x_t, u_t) 
> ```
这样我们就不用展开$J$去同时对$T$个控制变量求导, 也不用把所有状态$x_1,\cdots, x_T$通通用$x_0$和控制变量表示了, ==通过定义一个$Q(x,u,t)$完全包含后面一长串被当前决策变量和状态影响的未来奖励==, 进而获得当前时刻最优控制和状态的关系$u = Kx$, 这样我们就把求解一个线性方程组拆分成了$T+1$个子问题, 且每一步只需要对包含$u_t$的正定二次函数求解, 花费$O(k^3)$的计算量, 整个问题从$O((kT)^2)$缩短成$O(Tk^3)$的计算量 (==本质就是用动态规划求解矩阵运算O(∩_∩)O==) 

### 环境随机LQR问题

之前$x' = f(x,u)$是确定的, 这样通过`backward -> forward`得到的策略$u = \pi(t)$是一个只和时间和初始状态相关的量. 在现实中, 如果环境已知或well modeled, 不发生意外的话我们可以通过事先设计好一段程序, 让无人车按部就班执行; 但对于更复杂的问题, 例如在开放环境中同样预先设计的策略, 面对多变的路况也许并不适用, 应该设计一个更加灵活的$u = \pi(x,t)$这种dynamic policy(==接上了==)

对于状态转移方程而言
$$x' \sim p(x_{t+1} | x_t, u_t) = \mathcal{N}\left(F_t \begin{bmatrix} x_t \\ u_t \end{bmatrix} + f_t, \Sigma_t \right)$$

$V(x,t)$变成在期望意义下, $t$时刻处于状态$x$, 后续按照最优策略走, 获得的最小**期望**惩罚. 因为即使按照最优策略走后面的惩罚也不能事先确定. 同理$Q(x,u,t)$的定义也是如此. 然后步骤和确定性环境差不多, 用$V(s,t)$来替代还没发生的解, 进而迭代解出$V, Q$和$K$, 得到最优控制$x = K u$

### 非线性环境最优控制
现实中状态转移并非线性, 之前假设$x' = f(x,u) = Ax + bu$, 由于线性可加, $J$是一个关于$x_0, u_0, u_1, \cdots, u_T$的正定二次函数, 由于正定二次函数的凸性, 必有唯一的极值. 但一旦$f$是非线性的, $J$的展开式可能是复杂的非凸函数, 存在有多个局部最优点, 对于非凸函数, 即使已知表达式, 求出最优点也不容易. 

> 因为$V(x,t)$或者$Q(x,u,t)$方程过于复杂(非线性的缘故), 我们不能再使用基于价值的方式将大问题拆分成小问题, 因此我们转向基于策略的办法. 先随机生成一个$\mathbf{u}$, 然后在当前$\mathbf{u}$的局部寻找能把$J$缩小的局部最优解. 所以想法就是用泰勒展开把非线性函数表征成线性
> 
> 假设原本的状态是$\hat x_t$, 原本的控制是$\hat u_t$, 下一个状态是$f(\hat x_t, \hat u_t)$, 假设现在把当前状态改成
> $$x_t = \hat x_t + \delta x_t; \; u_t = \hat u_t + \delta u_t$$
> 于是我们把$f(x_t, u_t)$在$(\hat x_t, \hat u_t)$处泰勒展开, 就得到了一个关于函数变化$\delta f(x,u)$的LQR(f linear, cost quadratic), **为了消除高阶项, 假设**$\delta x_t \rightarrow 0, \delta u_t \rightarrow 0$
> ![泰勒展开](~@assets/rl_control-04.png#center)
> ```
> backward recursion
> state: δx, action: δu
> 
> forward pass
> δu = alpha (Kδx + k)
> ```
> 前面提到为了使用泰勒公式, local examination要保证$x, u$不能相差太远, 我们可以调整步长$\alpha$来控制$u_t - \hat u_t$, 但即使我们控制$u_t-\hat u_t, t = 0, \cdots, t$都很小, 他们的累积作用也可能使得$x_t - \hat x_t$偏差很大, 这样就不能满足局部线性假设(泰勒高阶项), 解决办法是用每次$u_t$只更新一步, 然后重新再做LQR, 这个方法叫做`replanning`, ==这个iterated LQR==算法值得我深入去研究一下, 这个倒不是局部最优和初始状态的问题, 而是`error compounding`导致改进太激进使得假设不满足的问题.
:::

## HJB方程

::: tip 时间连续的MDP
状态$x_t$和动作$u_t$不再是序列而是关于时间的连续函数, i.e., $x(t), u(t)$. 我们这里只考虑一个简单的情况： $f$是线性函数, $C, D$(单步损失, 最后惩罚)为正定二次函数
$$\begin{array}{ll}
\text{objective} & J = \int_0^T [x^T(t)Qx(t) + u^T(t)Ru(t)]dt + x^T(T)Dx(T)\\
\text{transition} & \dot x(t) = Ax(t) + Bu(t) \\
\text{initial} & x(0) = x_0 
\end{array}$$

> **价值函数**： 在离散时间MDP中, $V(x,t)$的定义是"在t时刻处于x状态下, 后续按照最优决策走, 能获得的最小损失". 这里定义差不多:
> $$\begin{aligned}
>   V(x(t)) &= \min_u \left[\int_t^T C(x(t),u(t))dt + D(x(T)) \right] \\
>           &= \min_u \left[\int_t^{t+dt} C(x(t),u(t))dt + V(x(t+dt)) \right] \tag{1}
> \end{aligned}$$
> 然后我们对$V(x(t+dt))$进行泰勒展开(注意这是一个关于$x_t$和$t$的函数), 这里主要利用了两个微积分知识, 当$d t \rightarrow 0$时
> 1. $\color{black} \int_{t}^{t+dt}fdt \approx f\cdot dt$
> 2. Taylor展开: $\color{black} V(t+dt, x+dx) \approx V(t,x) + \nabla_t V(t,x)  dt + \nabla_x V(t,x) dx(t)$
> 3. $\color{black} dx(t) = \dot x(t) dt$ 
> $$V(x(t+dt)) = V(x(t)) + \dot V(x(t))dt + \nabla_x V(x(t))\dot x(t)dt + o(dt)$$
>  将(1)代入到$V(x(t))$, 然后做差两边再除以$dt$
>  $$ 0 = \dot V(x(t),t) + \min_u [\nabla_x V(x(t),t)f(x(t),u(t)) + C(x(t), u(t))] \tag{2}$$ 

> **哈密尔顿量**: 这就是著名的H-J-B方程, 后面那个$\nabla_x V(x(t),t)\cdot f(x(t),u(t)) + C(x(t), u(t))$被称为"哈密尔顿量", $(\mathcal{H}(t))$, 最优控制为全局极值点, 一阶导数为$0 \Rightarrow \nabla_x V(x(t),t)f'_u(x,u) + C'_u(x,u) = 0$, 得到的最优控制是一个关于$x,t,V(x,t)$的函数, i.e., $u^\star(t) = \argmin_u \mathcal{H} = W(V(x,t),x)$

> **最终求解**: 将$u^\star$代入到(2)中, 求解一个关于$V(x,t)$的偏微分方程
> $$\begin{aligned}
>   \dot V(x,t) + \min_u[\nabla_x V(x,t)f(x, W(V(x,t),x) ) + C(x,W(V(x,t),x)) ] &= 0\\
>   V(x,T) &= D(T)
> \end{aligned}$$
> 求出$V(x,t)$后代入到$u=W(V(x,t),x)$中, 得到$u^\star(t) = K(x,t)$的表达式. 最后求解关于$x(t)$的常微分方程(forward recursion), 得到所有$x(0), x(1), \cdots$, 代入$u^\star = K(x,t)$中得到最优控制, 以上所有步骤总结在下面这个表中

### 具体例子
假设一个推箱子问题, 初始位置在$x(0)=x_0$, 要求在$t=T$时刻将箱子推到接近$x=0$的地方, 推箱子的单位距离能量耗损是$u(t)$, 非常简单的一个线性状态改变$\dot x(t) = x(t) + u(t)$, 我们的目标函数是
$$J = \int_0^T \frac{1}{4}u^2(t)dt + \frac{1}{4}x^2(T)$$

> 首先我们定义$V(x,t)$并列出H-J-B方程
> $$\dot V(x(t), t) + \min_u\left[\nabla_x V(x(t),t)[x(t) + u(t)] + \frac{1}{4}u^2(t) \right] = 0$$

> 然后我们求解汉密尔顿量(消除值函数中的`min`操作), i.e., $u^\star = \argmin_u \mathcal{H}$, 注意二次导数$>0$, 的确是极小值
> $$u^\star = -2\nabla_x V(x(t), t)$$

> 把$\mathcal{H}\rvert_{u = u\star}$带到原值函数里, 用$V_x$代表$\nabla_x V(x(t),t)$, $V_t$表征$\dot V(x(t),t)$, H-J-B方程变成
> $$\begin{aligned}
>   V_t + V_x[x(t) - 2V_x] + V^2_x &= 0 \\
>   V(x,T) &= x^2(T)/4
> \end{aligned}$$
> 这是一个关于$V(x,t)$的二元偏微分方程, 这个二元偏微分并不好解, 我们必须猜$V(x(t),t)$的形式

> 现在假设$V(x(t), t)$具有$\frac{1}{2}Q(t)x^2(t)$的形式, 其中$Q(t)$是随时间变化的正定矩阵, $V_x = Q(t)x(t)$, $V_t = \frac{1}{2}\dot Q(t)x^2(t)$(==奇怪为什么对时间的导数不包含状态本身呢==), 带到上面的方程里得到:
> $$\begin{aligned}
>   \frac{1}{2}\dot Q(t)x^2(t) - Q^2(t)x^2(t) + Q(t)x^2(t) &= 0 \\
>   \frac{1}{2}Q(T)x^2(T) &= x^2(T)/4
> \end{aligned}$$

> 现在假定$Q(t), x(t)$都是连续可导函数, $x_t$显然不可能处处为$0$, 因此两边消掉$x(t)$项, 用wolframe求得微分方程的结果为$Q(t) = e^{2T}/(e^{2t}+e^{2T})$
> ```
> DSolve[{x'[t]/2-x[t]^2+x[t] == 0, x[T] == 1/2}, x, t]
> ```
> 那么我们得到相应的$V(x,t) = \frac{1}{2}Q(t)x^2(t)$和最优控制$u^\star(t) = -2\nabla_x V(x(t), t) = -2Q(t)x(t)$

> 最后解关于$\dot x(t) = x(t) + u^\star(t), \; x(0)=x_0$的常微分方程, 同样用wolframe算得$x(t) = \frac{x_0 e^{2T}}{1+e^{2T}}e^{-t}Q^{-1}(t)$, 并且我们根据$x_t$和$u_t$的关系式, 得到$u^\star(t)$的最终表达式$u(t)= -2x_0e^{2T}/(1+e^{2T})\cdot 1/e^t$, 下面是整个过程的总结： 在离散时间问题中, 我们通过迭代
> $$V(x,t) = \min_u [ C(x,u) + V(f(x,u),t+1) ]$$
> 在backward recursion中求出所有$V(x,t)$, 然后在forward recursion中依次求出$u\star$; 而在连续问题中, 我们直接把$V(x,t)$的形式求出来(猜), 再通过优化关于$V$的$\mathcal{H}$来求出$u^\star$. 
> ![步骤-small](~@assets/rl_control-05.png#center)
:::

## 总结

::: warning introduction
总结一下MDP求解过程

1. 确定研究对象是策略$V_\pi, Q_\pi$还是价值$V,Q$. 他们都是衡量未来能够获得的期望效用. 另外还要看是否time-consistent, 注意==价值==强调的是要采取最佳动作条件下获得的回报, 因此我们有`max`操作. 
$$\begin{array}{ll}
    \text{1)} & V_\pi(s) = \sum_a\pi(a\vert s)[R(s,a)+\gamma\sum_{s'}P(s,a,s')V_\pi(s')] \\
    \text{2)} & V_\pi(s,t) = \sum_a\pi(a\vert s,t)[R(s,a)+\gamma\sum_{s'}P(s,a,s',t)V_\pi(s',t+1)] \\
    \text{3)} & V(s) = \max_a [R(s,a)+\gamma\sum_{s'}P(s,a,s')V(s')]\\
    \text{4)} & V(s,t) = \max_a [R(s,a)+\gamma\sum_{s'}P(s,a,s')V(s',t+1)]\\
\end{array}$$
2. 基本就是列出上面的式子, 包括立即奖励或损失$(R(a,s)$或者$C(x,u))$, 和后续的价值/策略价值$(\sum_{s'}P(s,a,s')V(s)$或者$Q(f(x,u),u,t+1))$
3. 对于时间连续的问题, 要用偏微分方程; 对于时间离散且又边界条件的情况, 用迭代法从边界条件出发依次求出其在整个定义域的取值, 对于只有方程没有边界条件的情况, 用雅阁比迭代收敛到最优. 最难的貌似是时间连续且环境随机的情况, 要使用随机微分方程的知识. 
:::


## 参考资料

[1] [强化学习轻松入门](https://www.zhihu.com/column/c_1266110382445654016)

