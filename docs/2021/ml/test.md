---
title: HJB
date: 2021-03-17
autoGroup-4: 强化学习
tags:
  - Knowledge
sidebarDepth: 3
---


## stochastic control problem

### introduction
::: tip introduction
> the core goal of the stochastic control problems is to maximize (or
minimize) certain expected profit (cost) functions by adjusting their own strategies that influence the dynamics of the underlying stochastic system
:::

<!-- ### optimal liquidation problem
::: warning
$$\begin{array}{ll}
    \mathcal{H}(x,S,q) &= \sup_{v \in \mathcal{A}}\mathbb{E}\left[X_T^v + Q^v_T(S_T^v - \alpha Q_T^v) - \phi \int_t^T (Q_s^v)^2ds \right] \tag{1} \\
    \text{inventory: } & dQ_t^v = -v_tdt, \; q_0 = \mathfrak{N} \\
    \text{price: } & dS_t^v = -g(v_t)dt + \sigma dW_t, \; S_0 = S \\
    \text{execution: } & \hat S_t^v = S_t^v - f(v_t), \; \hat S_0 = S \\
    \text{cash: } & dX_t^v = v_t\hat S_t^v dt, \; X_0 = x
\end{array}$$
- $\mathbf{v} = (v_t)_{0\leq t\leq T}$ is trading speed, which is the variable that agent controls to liquidate or acquire shares in the optimization problem and $v_t^\star$ denotes the optimal rate
- $\mathbf{Q^v} = (Q_t^v)_{0\leq t\leq T}$ is the agent’s inventory, which is affected by how fast the agent trades
- $\mathbf{W} = (W_t)_{0\leq t\leq T}$ is a Brownian motion
- $\mathbf{S^v} = (S^v_t)_{0\leq t\leq T}$ is the price process, and is affected primarily by the trading rates as well
- $\mathbf{\hat S^v} = (\hat S^v_t)_{0\leq t\leq T}$ is the execution price process, which the agent can sell/buy by walking the LOB
- $\mathbf{X^v} = (X^v_t)_{0\leq t\leq T}$ is the cash process resulting from the agent's execution strategy
- $g,f: \mathbf{R} \rightarrow \mathbf{R}^+$ denote the permanent and temporary price impact that agent's trading decisions has on the fundamental price and execution price respectively
- $\mathcal{A}$ is the admissible set of strategies: $\mathcal{F}$-measurable/predictable non-negative bounded strategies.
::: -->

