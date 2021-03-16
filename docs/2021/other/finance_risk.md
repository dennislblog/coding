---
title: Finance介绍
date: 2021-01-15
autoGroup-3: 知识 
categories:
  - Knowledge
tags:
  - Risk
sidebarDepth: 3
publish: true
---


::: tip
在这里记录金融学基本知识
:::

<!-- more -->

## 风险价值 (Value@Risk)
__定义__: 在市场正常波动下，某一金融资产或证券组合的最大可能损失。 更为确切的是指，在一定概率水平（置信度）下，某一金融资产或证券组合价值在未来特定时期内的最大可能损失(百度百科)。 常用的计算风险价值的方法是用历史数据去模拟, 根据在金融危机时期的回报数据去评估这些估计。
::: right
由于$p$往往设置的比较小，我们关注的因而是损失端的收益, <br>所以如果是`long position`在市场环境好的时候, VaR反而可能很高(波动大?)
:::


### 历史模拟 (Historical Simulation)
历史模拟法的基本思想是用给定历史时间段上所观测到的市场因子的变化来表示市场因子的未来变化。 相当于做一个历史回报的柱形图去置信估计今天的损失。

$$VaR_{t+1}^p = -\text{Percentile}\Big(\{R_{PF,t+1-\tau}\}_{\tau=1}^m, 100p\Big)$$

### 加权法 (Weighted Historical Simulation)
在上述历史模拟法中，每笔历史数据是等权重的。 但其实我们可以根据基金过去的业绩进行衰减加权，那么在预测未来上面会逐渐弱化历史久远的业绩表现。 每笔数据的权重，按$\eta$比率递减，且权重归一

$$\eta_\tau = \Big\{\eta^{\tau-1}(1-\eta)/(1-\eta^m)\Big\}_{\eta=1}^m$$


## 绝对/相对风险厌恶

::: tip 风险厌恶测量方法
选自[维基百科](https://en.wikipedia.org/wiki/Risk_aversion), 假设一个稳定投资可以获得$40$元, 而一个风险赌注有一半几率获得$100$元, 一半几率啥都没有, 期望收益是$50$元, 假设在他看来这两者没有区别的话, 我们可以认为他的效能函数满足: $u(40) = (u(0) + u(100))/2 = 50$, 也就是说此人最多愿意牺牲$10$元的期望价值, 已获得稳定的收益保障. 

$u(c)$的曲率越大(弯折程度), 越风险厌恶, 一种衡量风险厌恶的方法是"Arrow-Pratt measure of absolute risk-aversion, ARA", 定义是
$$A(c) = -\frac{u^{''}(c)}{u'(c)}$$
根据$dA/dc$, 即风险厌恶同资产的关系区分, 有三种形式:
1. CARA, 比如$u(c) = 1 - \exp(-\lambda c) \Rightarrow A(c) = \lambda$, 其风险厌恶水平一直保持在$\lambda$, 不随资产增加减少而变化, 比如银行?
2. DARA, 比如$u(c) = \log(c) \Rightarrow A(c) = 1/c$, 随着资产$c$的增加, 更愿意冒险了
3. IARA, 比如$u(c) = c - \lambda c^2 \Rightarrow A(c) = 2\lambda/(1-2\lambda c)$, 随着资产$c$的增加, 变得更保守, 比如辛辛苦苦打拼的事业?

另一种方法通过衡量此人愿意投入的资金占当前个人总资产比率的程度(中产和富豪不太可能玩一样的赌注), "Arrow–Pratt measure of relative risk aversion, RRA", 定义是
$$R(c) = -\frac{u^{''}(c)\cdot c}{u'(c)} = A(c)\cdot c$$
我们发现如果$R(c) \perp c$, 那么$A(c) = \frac{1}{c}$, 是一个DARA效能, 同样我们把相对风险厌恶分成三类
1. CRRA, 比如$u(c) = c^{1-\lambda} \Rightarrow R(c) = \lambda$, 无论总资产增加多少, 都定投(每个月拿总资产10%用来投资或消费)
2. DRRA, 比如$u(c) = (c-\eta)^{1-\lambda}-1/(1-\lambda) \Rightarrow R(c) = \lambda c/(c-\eta)$, 相对厌恶水平随总资产增加而降低, 越有钱消费比例更高, 这不是作死吗?
3. IRRA, 比如$u(c) = 1-\exp(-\lambda c) \Rightarrow R(c) = \lambda c$, 越有钱, 投资比例下降, 比如在加薪或市场景气的时候, 还是选择每月定投$100$元

<!-- to do: https://zhuanlan.zhihu.com/p/24311879 分析CYTHON的用法 -->
:::
