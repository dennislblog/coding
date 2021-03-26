---
title: 统计知识
date: 2021-03-26
autoGroup-1: 机器学习
categories:
  - Knowledge
tags:
  - Math
sidebarDepth: 3
---


::: tip
在这里总结统计知识
:::

<!-- more -->


## 分布

::::: tip 总结常见统计分布
参考资料
:::: tabs type: card
::: tab beta分布
> 对比二项式分布
> $$\begin{aligned}
    \text{Binomial} \qquad &  f(x) =  \binom{n}{x}p^x(1-p)^{n-x} \\
    \text{Beta} \qquad & g(p) =  \frac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1}
\end{aligned}$$
> 二项式分布对成功的次数进行建模, 贝塔分布则是对成功的概率$p$进行建模(概率是一个随机变量了), $\Beta(\alpha, \beta)$是贝塔分布PDF从$0\sim 1$图形下的面积.

![](~@assets/ml_stats-01.png#center)
> - $\alpha-1$就是成功的次数, $\beta-1$就是失败的次数, 随着$\alpha \nearrow$(成功次数增多), 概率分布向右边移动, 代表成功超过$p$的可能性变大. 
> - 当我们设置$\alpha=1$时, 则代表历史上没成功过, 那么我们会得到一个向下的直线PDF, 代表说成功率大于$p$的可能性直线下降
> - 当$\alpha < 1,\beta < 1$时, 我们得到倒U型PDF, 怎么理解? 比如$\alpha=\beta=0.5$, 那么贝塔描述的就是重复$\alpha,\beta$概率这样一个实验, 最后成功次数多于失败次数的概率估计. 但还是不能解释为啥$\Beta(0.2,0.8)$在结尾有一个陡升
> - 之前讲过$\Beta(\alpha, \beta)$数值上是图行的AUC, ==beta和gamma的关系有待理解==
> $$\Beta(\alpha, \beta) = \int_0^1 x^{\alpha-1}(1-x)^{\beta-1}dx = \frac{\alpha-1}{\beta}\Beta(\alpha-1, \beta+1) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)} $$
:::
::: tab gamma分布
|  指数分布：  | 等一个随机事件发生, 需要经历多久时间  | 
|  :----  | :----  |
|  伽玛分布：  | 等N个随机事件都发生, 需要经历多久时间, 就是上面N个相互独立变量的和 |

$$\begin{aligned}
    \text{exponential} \qquad &  f(x) =  \lambda e^{-\lambda x}, x>0 && \mathbb{E}[x]=\lambda^{-1}, \mathbb{V}[x]=\lambda^{-2} \\
    \text{gamma} \qquad & f(x) = \frac{1}{\Gamma(\alpha)} \lambda^{\alpha}x^{\alpha-1} e^{-\lambda x}, x>0 && \mathbb{E}[x]=\lambda^{-1}\alpha, \mathbb{V}[x]=\lambda^{-2}\alpha
\end{aligned}$$

> 伽玛分布与伽玛函数
> - 伽玛函数： $\Gamma(\alpha) = \int_0^\infty x^{\alpha-1}e^{-x}dx$
> 证明 $\int_0^\infty x^{\alpha-1}e^{-\lambda x} dx = \Gamma(\alpha)/\lambda^2$ (把$y = \lambda x$换元即可)

![](~@assets/ml_stats-02.png#center)
> 伽玛分布的意义
> - 指数分布的意义在于, 随着间隔时间变长, 事件的发生概率急剧下降(比如每隔5分钟出现一辆车和每隔5小时才出现一辆车的概率是线性下降的吗), 呈指数式衰减
> - 当$\alpha=1$, 伽玛分布就是指数分布. 假设平均每隔5分钟出现一辆车(即衰减率为$\lambda = 0.2$), 那么每隔至少10分钟出现两辆车的概率$P(X > 10) = 0.406 < 0.5$, 9分钟可能就有超过一半概率观察到两辆车了
:::
::::
:::::