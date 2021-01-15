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
在上述历史模拟法中，每笔历史数据是等权重的。 但其实我们可以根据基金过去的业绩进行衰减加权，那么在预测未来上面会逐渐弱化历史久远的业绩表现。 每笔数据的权重，按λ比率递减，且权重归一

$$\eta_\tau = \Big\{\eta^{\tau-1}(1-\eta)/(1-\eta^m)\Big\}_{\eta=1}^m$$


<!-- to do: https://zhuanlan.zhihu.com/p/24311879 分析CYTHON的用法 -->

