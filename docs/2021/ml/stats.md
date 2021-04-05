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

::::: tip 
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


## 随机过程
::: right
随机过程（Stochastic Process）如果一个变量$z$的值，以不确定形式随时间$t$变化，我们称这个变量服从某种随机过程
:::

::::: tip 
:::: tabs type: card
::: tab 布朗运动
![](~@assets/ml_stats-03.png#right)
> - 如果定义随机过程$W = \{W_t, t\geq 0\}$满足
> 1. $W_0 = 0$, 初始值
> 2. $\forall s < t, W_t - W_s \sim \mathcal{N}(0, t-s)$且相互独立
> 3. 两个随机过程的相关$R(s,t) = \min(s,t)$ 
> 4. 标准布朗的形式是$\alpha W_t + \beta$, 其中$W_t$是维纳过程, 即标准布朗运动
>
> - __性质__
> 1. 布朗运动连续，但处处不可微
> 2. 对称性, $-W_t$也是布朗; 自相似性: 对于任意$a>0, W_{at} = a^{1/2}W_t$
> 3. 马尔科夫性质: 原本我们计算对未来的期望$f(X_t),t>s$, 需要过去所有时刻的信息流$\mathcal{F}_s$, 而作为马尔科夫过程, 只需要当前时刻的信息$\sigma(X_s)$. 最重要的结论是**将来的概率分布不依赖过去的值和路径**
>
> - __布朗桥__: 对于$t \in [0,1]$, 定义$B_t = W_t - tW_1$, 则称随机过程$B_t, t\geq 0$为$0 \rightarrow 0$的布朗桥
> 1. 均值为$0$, 相关系数$R(t,s) = t - ts, t < s$
:::
::: tab 莱维过程 
> ![](~@assets/ml_stats-05.png#right)
> - 如果定义随机过程$L = \{L_t, t \geq 0\}$满足
> 1. $L_0 = 0$, 初始值
> 2. $\forall s < t, a > 0, P(|L(t)-L(s)| > a) > 0$ 且相互独立
> 3. 布朗过程是莱维过程里唯一路径连续的例子? 莱维过程 = linear drift + diffusion(weiner?gamma?) + jumps
> 
> - 把一个布朗随机变量用伽玛过程采样, 得到一个方差伽玛过程(variance gamma process)
> $$X_t = \theta t + \sigma W_t; \; X_{\gamma_t} = \theta \gamma_t + \sigma W_{\gamma_t}$$
> 比如我们对节假日的出现用伽玛过程描述 $f(x; \alpha, \theta) = \frac{x^{\alpha-1} e^{-x/\theta}}{\Gamma(\alpha) \theta^\alpha}, \quad x > 0$

:::
::::
::: details Julia
```julia
#= 
Define Gamma process (输入γ和λ), 对应的伽玛函数 shape α = t*γ; scale θ = 1/λ
A GammaProcess with 
1. jump rate γ and inverse jump size λ 
2. has increments Gamma(t*γ, 1/λ) 
3. and Levy measure ν(x)=γ 1/x exp(-λx)

tt = range(0, stop=1, length=1000)  # 创建一个0->1, 1000个点
G  = GammaProcess(10., 1.)          # γ=10, λ=1, 增量~Gamma(tγ, 1/λ)
GB = GammaBridge(1., 2., G)         # (hitting) v=2 at t=1, Gamma Process

=#
function sample(tt::AbstractVector{Float64}, P::GammaBridge, x1::Float64 = 0.0)
    tt = collect(tt)
    t = P.t
    r = searchsorted(tt, t)
    if isempty(r) # add t between n = last(r) and first(r)=n+1
       tt = Float64[tt[1:last(r)]; t; tt[first(r):end]] # t now at first(r)
    end
    X = sample(tt, P.P, zero(x1))
    dx = P.v - x1
    yy = X.yy
    yy[:] =  yy .* (dx/yy[first(r)]) .+ x1
    if isempty(r) # remove (t,x1)
        tt = [tt[1:last(r)]; tt[first(r)+1:end]]
        yy = [yy[1:last(r)]; yy[first(r)+1:end]]
    end
    SamplePath{Float64}(tt, yy)
end
```
:::
:::::

