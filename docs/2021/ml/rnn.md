---
title: 循环神经网络
date: 2021-02-09
autoGroup-3: 深度学习
tags:
  - Knowledge
---

::: tip
在这里记录RNN, LSTM, GRU相关知识
:::

<!-- more -->

## LSTM

![LSTM](~@assets/ml_rnn-1.jpg)

由Hochreiter 和 Schmidhuber（1997）介绍引入。 不同于RNN单元中只是一个简单的`tanh`激活函数。 LSTM则通过门控的思想过滤信息, 比如$\sigma \in [0,1]$选择筛选信息量

:::: tabs type: card
::: tab 遗忘门
![forget gate](~@assets/ml_rnn-2.png)
- 假设这个任务是一个基于上文预测最后一个词的语言模型
- 上一个词的隐态和当前词, 确定要不要遗忘当前主题$C_{t-1}$的信息
:::
::: tab 输入门
![input gate](~@assets/ml_rnn-3.png)
- 第一个输入门$i_t$决定哪些数据需要更新
- 一个$\tanh \in [-1,1]$, 生成新的主题, 然后用$\sigma$去控制要不要把新的语言主题信息加入到单元状态中, 以替代我们要遗忘的主题
- 新的单元状态 = 遗忘旧的状态 + 新的及意义信息
    $$C_t = f_tC_{t-1} + i_t\tilde C_t$$
:::
::: tab 输出门
![output gate](~@assets/ml_rnn-4.png)
- 最后把新的单元状态, 再通过一个$\tanh$, 把输出限制在$[-1,1]$, 然后和$\sigma$的权重相乘, 得到下一个隐态
:::
::::

### LSTM如何防止梯度消失和梯度爆炸

由于导数的链式法则, 如果导数都是小数或者都大于$1$, 则会使得总体度消失或者爆炸, 如果只是梯度爆炸, 还可以通过`gradient clipping`限制范围的方法来解决, 

但梯度消失则没办法, 而LSTM中的单元状态$S_t = \sum_{\tau = 1}^t \Delta S_{\tau}$, 他的导数不再是乘积的形式, 就可以避免了


## GRU

![GRU](~@assets/ml_rnn-5.jpg)

循环门单元（Gated Recurrent Unit）由 Cho, et al. (2014)提出。 主要是简化LSTM单元的结构: 将遗忘和输入合并到一个门, 并且合并了单元状态和隐态

- 这里的候选隐藏层(candidate hidden layer) $\tilde h_t$ 和 LSTM中的 $\tilde C_t$ 类似, 可以看成当前时刻的新信息
- GRU没有输出门(==把$C_t$单元状态整个一行给拿掉了==), 通过候选和前一时刻的隐藏层得到这一时刻的隐藏层信息
    $$h_t = (1-z_t)h_{t-1} + z_t\tilde h_t$$
- 一般来说短距离相关的单元`重置门`活跃($r_t=1, z_t=0$就相当于RNN了), 而长距离依赖的单元`更新门`活跃

:::: tabs type: card
::: tab 重置门
控制保留多少之前的记忆
$$r_t = \sigma(W_r x_t + U_r h_{t-1})$$
:::
::: tab 更新门
控制需要从前一个时刻的隐藏层$h_{t-1}$中保留多少信息
$$z_t = \sigma(W_zx_t + U_z h_{t-1})$$
:::
::::

