---
title: 简介
date: 2020-01-05
autoGroup-2: 论文
categories:
  - Paper
tags:
  - Thesis
publish: false
sidebarDepth: 2
---

::: tip
在这里记录我论文的进展
:::

<!-- more -->

![论文框架](~@assets/thesis-01-1.png#center)

## 摘要

由于各种原因，金融机构在买卖资产时经常利用高级交易策略。 机器学习被广泛应用在买卖资产优化问题中
~~我的研究目的是~~ 但很少有涉及日内交易的算法研究。如果金融信号噪音太多，使得算法难以掌握内在的规律，是否可以考虑先抽象出具体规则，然后再用神经网络去学习这个规律呢？

本文涉及的主要问题是如何在`一个小时内，优化交易，以最少的交易成本，减持百分之十的股份`。 我们会分成三个研究来做： 1. 探讨什么样的价格影响数学模型，对交易策略最敏感；2. 深度网络是否可以被用来学习这个模型(比如没有足够多的数据)；3. 是否能用强化学习把此过程转换为端到端的学习管道，并且增加模型的鲁棒性。 如果有额外精力，可以探讨限价单策略(当前只考虑市场单策略)。 此外，我们定义了一个评估程序，该程序可以确定强化学习代理所学习的策略的功能和局限性，不断优化这个模型。


## 交易成本的数学模型

### Almgren and Chriss (2000)

![AC价格影响模型](~@assets/thesis-01-2.png#center)

在**期望-方差**框架下，[Almgren 和 Chriss （2000）](https://www.math.nyu.edu/faculty/chriss/optliq_f.pdf)认为交易行为会对价格带来两种影响： 1） 永久性影响（Permanent Impact) 2) 暂时性影响 （Temporary Impact)。 前者会持续性对未来价格迭代产生影响，后者只是当前的影响，不会出现对未来的价格产生影响。

> 举个例子：假设不考虑其他因素，某股票交易在前为100元。本屌卖了10单，如果我这次交易的永久性影响是-10元，暂时性影响是-1元，那么我当下的每股交易成本是100-10-1 = 89 元，但下一时刻，股价变为90元。


__价格函数__

:::: tabs
::: tab math
价格随订单策略的变化 (暂时影响不影响价格变化)
$$\begin{aligned}
	P_{t} &= P_{t-1} - \sigma\sqrt{\tau}\cdot \xi_t - \tau g\Big(\frac{n_t}{\tau}\Big) \\
	g(v)  &= \gamma v
\end{aligned}$$
> 关于参数$\gamma$的选择, 通常的原则是当交易量达到日均交易总量的10%时, 这次交易将影响整个市场对这只股票的估值, 即永久影响。 ~~至于这个影响是多大呢?~~, 每10%影响一个利差基点(即买卖利差)

:::
::: tab code
```python
info.price = self.prevImpactedPrice + np.sqrt(self.singleStepVariance * self.tau) * random.normalvariate(0, 1)
self.prevImpactedPrice = info.price - info.currentPermanentImpact
info.currentPermanentImpact = self.permanentImpact(info.share_to_sell_now)
def permanentImpact(self, sharesToSell):
    pi = self.gamma * sharesToSell
    return pi
```
:::
::::

> 成交价格是 $P'_t = P_t - \epsilon \cdot \text{sgn}(n_t) + \frac{\eta}{\tau}n_t$, 其中$\epsilon$是固定交易成本(例如收取半个买卖价差的中介费), 不考虑交易量的大小。 $\eta$代表单位成交量对市场的短暂冲击，由市场流动性本身和交易间隔大小共同决定(间隔$\tau$越短，不利影响越大)

__期望成本__

从期望成本的公式来看，前面两项基本是不变的(除非卖不完), 第三项很有意思, 交易量主要冲击短期价差, 但会受到长期价格影响的抵消作用(怎么解释?相反作用力?)

:::: tabs
::: tab math
在线性(短期和长期影响)模型下的期望成本和方差随交易策略$\langle \mathbf{n} \rangle_t$的函数(来自论文`Eq(4)`和`Eq(5)`)

| $n_t$ | $t$时刻卖 | $x_t$ | $t$时刻还剩 | $\tau$| 单次交易时间 |
| -----:| :---- | ----: | :---- | ----: | :---- |
| $\gamma$ | kyle影响 | $\eta$| 每1%交易量产生的暂时影响 | $\epsilon$ | 中介费 |

$$\begin{aligned}
	\mathbb{E}(x) &= \sum\tau x_t g\Big(\frac{n_t}{\tau}\Big) + \sum n_t h\Big(\frac{n_t}{\tau}\Big)\\[1em]
				  &=  \frac{1}{2}\gamma X^2 + \epsilon\sum|n_t| + \frac{\eta-0.5\gamma\tau}{\tau}\sum n_t^2 \\[1em]
	\mathbb{V}(x) &= \sigma^2\sum\tau x_t^2 
\end{aligned}$$
:::
::: tab code
```python
def get_expected_shortfall(self, sharesToSell):
    # Calculate the expected shortfall according to equation (8) of the AC paper
    ft = 0.5 * self.gamma * (sharesToSell**2)        
    st = self.epsilon * sharesToSell
    tt = (self.eta_hat / self.tau) * self.totalSSSQ
    return ft + st + tt
info.expected_shortfall = self.get_expected_shortfall(self.total_shares)
info.expected_variance = self.singleStepVariance * self.tau * self.totalSRSQ
self.totalSSSQ = sum(info.share_to_sell_now**2)
self.totalSRSQ = sum(self.shares_remaining**2)
```
:::
::::

__两个特例__

:::: tabs
::: tab 最小期望
为何均匀抛售(即TWP策略?)使交易成本期望最小呢? 答案就是解上面的二元一次方程组, 当$n_1 = n_2 ... = n_T = \frac{X}{N}$的时候, 二次项最小

$$\begin{aligned}
	\mathbb{E}(x) &= \frac{1}{2}\gamma X^2 + \epsilon X + (\eta - \frac{1}{2}\gamma\tau)\frac{X^2}{T} \\[0.5em] 
	\mathbb{V}(x) &= \frac{1}{3}\sigma^2X^2T\Big(1-\frac{1}{N}\Big)\Big(1-\frac{1}{2N}\Big)
\end{aligned}$$
:::
::: tab 最小风险
还是看公式, 风险最小就是 $x_1 = x_2 ... = x_T = 0$, 即第一次就清空所有任务量。

$$\begin{aligned}
	\mathbb{E}(x) &= \epsilon X + \eta\frac{X^2}{\tau} \\[0.5em] 
	\mathbb{V}(x) &= 0
\end{aligned}$$
:::
::::

__一般情况__

在**期望-风险**框架下，我们希望解一般形式(即$\mathbb{E}(x) + \lambda \mathbb{V}(x)$), 把交易量用剩余量表示$n_t = x_{t-1}-x_t$, 然后对$x_t$求导，得到一个二阶差分方程

$$x_{t-1} + b x_t + x_{t+1} = 0$$

其中$b = 2 + \lambda\sigma^2\tau^2(\eta - 0.5\gamma\tau)^{-1}$，因此在一定市场流动性($\eta$), 交易间隔($\tau$), 股票风险($\sigma$)和交易员风险偏好($\lambda$)的作用下, 交易员有一个最优的交易策略

::: details 解差分方程
__例子__： 求$y_{t+2} - 5y_{t+1} + 6y_t = 0$, 已知$y_0 = 2, y_1 = 5$

__解__： 特征方程 $\lambda^2 -5\lambda + 6 = 0$ 解得 $\lambda_1 = 2, \lambda_2 = 3$ 

解析解就是 $y_t = C_1 2^t + C_2 3^t$ 没有周期性(因为有解, 否则涉及复数)。 把$y_0, y_1$的特殊情况带进去得到 $y_t = 2^t + 3^t$

在这里我们用[同样的方法](https://www.cnblogs.com/TaigaCon/p/6879479.html)，因为$b\geq 2$, 因此没有周期性(即在终止点$x_T=0$之前不存在另一个$x_t=0$, 提前结束任务的情况)。 同样解得 $\lambda_1 = \frac{1}{2}(-b-\sqrt{\Delta}), \lambda_2 = \frac{1}{2}(-b+\sqrt{\Delta})$，把$x_0 = X, x_T = 0$带进去, 得到

$$x_t = \frac{\lambda_2^T}{\lambda_2^T-\lambda_1^T}X\cdot \lambda_1^t - \frac{\lambda_1^T}{\lambda_2^T-\lambda_1^T}X\cdot \lambda_2^t$$

假设$b$刚好等于$2$, 即无风险厌恶的交易员, 那么此时$\lambda$为重根, 差分方程的齐次解为$x_t = (C_1 + C_2 t)\cdot(-1)^{t}$, 由初始条件判定

$$\begin{aligned}
	C_1 &= X
	(C_1 + C_2T)\cdot(-1)^{T} &= 0
\end{aligned}$$
那么$C_2 = \frac{X}{T}$, 但我希望得到的是$X - \frac{t}{T}X$呀，不知道哪里错了
:::

__最优解__

:::: tabs
::: tab math
![efficient frontier](~@assets/thesis-01-3.png#center)

按照上面的方法得到一般解(来自论文`Eq(20)`) 那个切线就是交易员的风险偏好产生的`utility` = $E + \lambda V$
$$\begin{aligned}
	\mathbb{E}(x) &= \frac{1}{2}\gamma X^2 + \epsilon X + (\eta - 0.5\gamma\tau)X^2\tanh(0.5\kappa\tau)\Big(\tau\sinh(2\kappa T) \\[0.5em]
	&+ 2T\sinh(\kappa\tau)\Big)(2\tau^2\sinh^2(\kappa T))^{-1} \\[1em]
	\mathbb{V}(x) &= \frac{1}{2}\sigma^2X^2\Big(\tau\sinh(\kappa T)\cosh(\kappa(T-\tau))-T\sinh(\kappa\tau)\Big) \\[0.5em]
	&\cdot \sinh^{-2}(\kappa T)\sinh^{-1}(\kappa\tau)\\[1em]
	n_t &= x_{t-1}-x_t = 2\sinh(0.5\kappa\tau)\cosh(\kappa(T-t_{j-0.5}))X\sinh^{-1}(\kappa T) 
\end{aligned}$$
:::
::: tab code
```python
def get_AC_expected_shortfall(self, sharesToSell):
    ft = 0.5 * self.gamma * (sharesToSell ** 2)        
    st = self.epsilon * sharesToSell        
    tt = self.eta_hat * (sharesToSell ** 2)       
    nft = np.tanh(0.5 * self.kappa * self.tau) * (self.tau * np.sinh(2 * self.kappa * self.liquidation_time)  + 2 * self.liquidation_time * np.sinh(self.kappa * self.tau))       
    dft = 2 * (self.tau ** 2) * (np.sinh(self.kappa * self.liquidation_time) ** 2)   
    return ft + st + (tt * nft / dft) 
def get_AC_variance(self, sharesToSell):
    ft = 0.5 * (self.singleStepVariance) * (sharesToSell ** 2)                        
	nst  = self.tau * np.sinh(self.kappa * self.liquidation_time) * np.cosh(self.kappa * (self.liquidation_time - self.tau)) - self.liquidation_time * np.sinh(self.kappa * self.tau)
	dst = (np.sinh(self.kappa * self.liquidation_time) ** 2) * np.sinh(self.kappa * self.tau)
    return ft * nst / dst
def get_trade_list(self):
    trade_list = np.zeros(self.num_n)
    ftn = 2 * np.sinh(0.5 * self.kappa * self.tau)
    ftd = np.sinh(self.kappa * self.liquidation_time)
    ft = (ftn / ftd) * self.total_shares
    for i in range(1, self.num_n + 1):       
        st = np.cosh(self.kappa * (self.liquidation_time - (i - 0.5) * self.tau))
        trade_list[i - 1] = st
    return trade_list * ft
```
:::
::::


!!!include(./thesis/chapter_01_intro.md)!!!