---
title: 数学知识
date: 2021-02-04
autoGroup-1: 机器学习
categories:
  - Knowledge
tags:
  - Math
sidebarDepth: 2
publish: true
---

::: tip
在这里总结数学知识
:::

<!-- more -->


## 范数

:::::: tip 通常用范数来解决过拟合问题
::::: tabs type: card
:::: tab 向量
对于向量$x=[x_1, x_2, ..., x_m]$, $\|x\|_p$可以表示为

|  p=1   | 向量元素绝对值之和 $\|x\|_1 = \sum_{i=1}^m \vert x_i\vert$ |
|  :---- | :----  | 
|  p=2   | 向量到零点的欧式距离 $\|x\|_2 = \sqrt{\sum_{i=1}^m x_i^2}$ |
|  p=∞   | 所有向量元素绝对值中的最大值 $\|x\|_{\infty} = \max_i \vert x\vert$ |
|  p=-∞  | 所有向量元素绝对值中的最小值 $\|x\|_{-\infty} = \min_i \vert x\vert$ |
|  p=0   | 非零元素的个数 $\|x\|_0 = \text{count}(x_i != 0)$ |

```python
from sympy import *
x = Matrix([-10, 2, 100])
x.norm(oo); x.norm(1); x.norm(2).evalf().round(2)
>> 100, 112, 100.52
```
::::
:::: tab 矩阵
对于矩阵$A \in \mathbb{R}^{m \times n}$

|  p=1   | 所有矩阵列向量绝对值之和的最大值 $\|A\|_1 = \max_j \sum_{i=1}^m \vert a_{i,j}\vert$ |
|  :---- | :----  | 
|  p=2   | $A^TA$的最大特征根, $\|A\|_2 = \sqrt{\lambda_1}$ |
|  p=∞   | 所有矩阵行向量绝对值之和的最大值 $\|A\|_{\infty} = \max_j \sum_{j=1}^m\vert a_{i,j}\vert$ |
|  p=F   | Frobenius范数, 矩阵元素绝对值的平方和再开平方 $\|A\|_F = \left(\sum_{i=1}^m\sum_{j=1}^n a_{i,j}^2\right)^{1/2}$ |

```python
"""
    5   2   1
    3   3   3
    2   5   1
"""
m = ImmutableDenseMatrix([[5, 2, 1], [3, 3, 3], [2, 5, 1]])
m.norm(oo); m.norm(1); m.norm(2).evalf().round(2)
>> 9, 10, 5√3
```
::::
:::::
::::::

## 微积分
::::: tip 微积分小记
:::: tabs type: card
::: tab 分部积分
核心公式
$$\int uv' dx = uv - \int u'v dx$$
- 求高脚本的容积? 其侧壁的曲线函数$y=\exp(x)$, 半径从$0$到$1$的圆
$$\begin{aligned}
    V &= \int_1^e \pi (\ln y) dy \\
      &= (\pi y\ln^2 y)\vert_1^e - 2\pi\int_1^e \ln y dy \\
      &= \pi(y\ln^2 y - 2y\ln y + 2y)\vert_1^e = \pi(e - 2)
\end{aligned}$$
:::
::: tab 矩阵微分
<!-- ![](~@assets/ml_math_04.png#center) -->
[参考大神写的资料](https://explained.ai/matrix-calculus/index.html#reference), 
我自己也写了[一份](~@assets/math-matrix_derivative.pdf)
- Kronecker product $\otimes$(\otimes): 张量乘积, 逐一匹配
- Hadamard product $\circ$(\circ): 对应位置元素相乘

假设我们现在有一个矩阵$\mathbf{X}$,
- $\mathbf{M}_{i,j}$ 代表矩阵的镜像, 是去掉第$i$行和第$j$列之后, 剩余矩阵的行列式(determinant)
- $\mathbf{C}_{i,j} = (-1)^{i+j}\mathbf{M}_{i,j}$ 被称作cofactor matrix
- $\color{black} adj(\mathbf{X}) = C^T$, 在求逆矩阵时会用到(if X is invertible), 
$$\mathbf{X}^{-1} = \text{adj}(\mathbf{X})/\det(\mathbf{X}) \Rightarrow \left(\mathbf{X}^{-1}\right)^T_{i,j} = \frac{1}{\det \mathbf{X}}\mathbf{C}_{i,j}$$

- $\det \mathbf{X} = \sum_{k=1}^{n} X_{ik}C_{ik}$, by the production rule
$$\frac{\partial \det \mathbf{X}}{\partial X_{ij}} = \sum_{k=1}^{n} \left(\frac{\partial X_{ik}}{\partial X_{ij}}C_{ik} + \frac{\partial C_{ik}}{\partial X_{ij}}X_{ik}\right)$$
> $\partial X_{ik}/\partial X_{ij} = 1$ if $k = j$ otherwise $0$, 所以第一项结果就是$C_{ij}$, 而后面那一项根据$C_{ij}$的定义, 是抠掉了$i$行和$j$列的镜像值, 因此$\partial C_{ik}/\partial X_{ij} = 0 \quad \forall k$, 所以我们有
> $$\frac{\partial \log \det \mathbf{X}}{\mathbf{X}} = \frac{1}{\det \mathbf{X}}\frac{\partial \det \mathbf{X}}{\partial X_{ij}} = \frac{C_{ij}}{\det \mathbf{X}} = (X^{-1})^T_{ij}$$
:::
::::
:::::


## 基本数学

::::::: tip 暂时未归类
:::::: tabs type: card
::: tab sigma域

概率空间由样本空间$\Omega$, 事件集合$\mathcal{F}$和概率测度$\mathcal{P}$组成

- 样本空间： 试验中所有可能结果的集合，每个结果互斥，所有可能结果必须被穷尽
- 事件集合： 由样本空间的一些子集构成的集合, 必须是$\sigma$-field, 即包含三点特性
    + 必须包含不可能事件
    + 事件的互补事件必须也被包含
    + 事件的union合集也必须被包含
- 概率测度： 描述一次随机试验中被包含在**事件集合**中的所有事件的可能性, 也对应上面的三个特性
    + 概率在 0 到 1 之间
    + 总的样本空间概率为1 (由事件集合的第1,2推出)
    + 如果事件互斥, 那么联合概率等于概率的和 (由事件集合的第3推出)

__例子__： 一辆车从$12:00$到$01:00$的任何时间都可以到达, 这时$\Omega$有无穷多个, 并且还不可数(无穷但按照某种标准如大小编号, 可以把他们数完), 那么就没有办法对任何一个结果$\omega$分配一个概率, 但是直觉会告诉你概率表达式应该是这个样子(正好符合事件集合的三个特性, $\sigma$-field)
$$P([x_1, x_2]) = x_2 - x_1, \quad \forall 0 \leq x_1 \leq x_2 \leq 1$$
:::
::: tab Jansen不等式
如果$f$是凸函数：
$$f\left(\sum_{i=1}^k w_i x_i\right) \leq \sum_{i=1}^k w_i f(x_i)$$
比如我在论文里看到的这个(因为 $yh(y)$ 是凸函数)
$$\sum_{t=1}^T \frac{x_t}{\eta_t}h\left(\frac{x_t}{\eta_t}\right)\eta_t \geq \left( \sum_{t=1}^T \frac{x_t}{\eta_t} \eta_t \right)h\left( \sum_{t=1}^T \frac{x_t}{\eta_t} \eta_t \right)$$
:::
::: tab ROC相关
准确率(accuracy) = 多少分类准确 (TP+TN)/(TP+TN+FP+FN)

精确率(precision) = 你认为正例的样本中, 有多少猜对了 (TP)/(TP+FP)

召回率(recall) = 真实的正例样本中, 有多少被你找出来了 (TP)/(TP+FN)
:::
::::::
:::::::

## QR 分解
::::: tip 分解有啥用, 除了加速运算
:::: tabs type: card
::: tab Gram-Schmidt 正交分解

两个向量的内积 $x^T y = \| x \|\| y \| \cos\theta$, 下面$v_2$代表$x_2$减掉其在$v_1$上的投射, 与$v_1$垂直的向量

![](~@assets/ml_math_01.svg#center)
```python
def gram_schmidt(X):
    n, k = X.shape
    Q, I = np.empty((n,k)), np.eye(n)
    v1 = X[:,0]; Q[:, 0] = v1/np.sqrt(np.sum(v1*v1))
    for i in range(1, k):
        # now project onto the orthogonal complement of col span 
        #     x: the vector to project, the first i-1 col-span of X
        x, V = X[:, i], X[:, 0:i]
        v = (I - v @ np.linalg.inv(V.T @ V) @ V.T) @ b
        Q[:, i] = v/np.sqrt(np.sum(v * v))
    return Q
```
:::
::: tab 分解原理
1. $A = QR$, Q是一个正交矩阵(Q'Q = I), R是一个上三角矩阵(矩阵对角线下面的元素全是0)
![](~@assets/ml_math_02.png#center)
2. 正交矩阵对欧式范数结果不影响 
$$\|Qv\|_2^2 = v'Q'Qv = v'v = \|v\|_2^2$$
3. 用上面的Gram-Schmidt方法得到正交矩阵$Q$, 利用正交的性质
$$A = QR \Longrightarrow R = Q^{-1}A = Q'A$$

Q: 求把 $y= [1,3,-3]^T$ 投射到 $X = \left(
\begin{array}{cc}
    1 &  0  \\
    0 & -6 \\
    2 &  2
\end{array}
\right)$ 上的向量

向量投射向量只需要求 $\|y\|\cos\theta = \frac{x'}{\|x\|}y$ 即可
- $Xa$的含义就是在平面$X$上的线性组合, 得到平面上的一条直线, 如果$b$这个点正好在平面上, 残差就是0, 但是如果不在$X$平面上, 我们希望$e =b-Xa$尽量短, 当这个$e \perp X$时残差$\sqrt{e'e}$最小
- 因此最小二乘法就是构建与$X$平面垂直的残差: 
$$(b-Xa)'X = 0 \Rightarrow a = (X'X)^{-1}X'b$$

下面两种办法都可以, 但第二种方法更快. 为什么第二种方法更快而且更准? 因为$Q$矩阵的条件数更小(更稳定, 不至于浮点溢出), i.e., $\kappa(Q) = \|Q^{-1}\|\cdot \|Q\|$, 若我们用norm-2, 则条件等于矩阵$Q$最大奇异值和最小奇异值的比. 另外如果行数大于列数, 这种情况叫做**overdetermined**

```python
"""
y = [1, 3, -3]
X = [[1,  0], [0, -6], [2,  2]]
"""
# 1. Py = X @ inv(X'X) @ X' @ y, (y-pY) ⊥ X
X @ np.linalg.inv(X.T @ X) @ X.T @ y
>> array([-0.56521739,  3.26086957, -2.2173913 ])

# 2. Q-R Decomposition Q @ Q.T @ y
import numpy as np
Q, R = np.linalg.qr(X)  #Q.T @ Q = I, 
Q @ Q.T @ y
>> array([-0.56521739,  3.26086957, -2.2173913 ])
```
:::
::::
:::::

## 马尔科夫

:::::: tip 介绍
::::: tabs type: card
:::: tab 基本介绍
马尔科夫矩阵: $n x n$, 所有元素非负, 每一行加起来都是$1$

马尔科夫性质： $P(X_{t+1} = y \vert X_t) = P(X_{t+1} = y \vert X_{1:t}$ 当前状态概率只和前一个状态相关

__例子__： 在一个月时间里, 失业工人找到工作的概率$\alpha \in (0,1)$, 在职工人失去工作的概率$\beta \in (0,1)$, 状态 S = (失业, 就业) = (0, 1), 状态转移方程 $P = \left( \begin{array}{cc} 1 - \alpha & \alpha \\ \beta & 1 - \beta \end{array} \right)$

现在回答三个问题
1. 平均失业时间 $p = \beta / (\alpha + \beta)$
2. 长期来看, 一个工人多久时间会处于失业
3. 一个在职工人在未来12个月里失去工作的概率

```python
"""
基于 quantecon.random.draw(cdf, n_sim) 得到, where cdf = cumsum(P[state])
"""
import quantecon as qe
P = [[0.4, 0.6], [0.2, 0.8]]  #状态转移方程, 失业->在职 = 0.6
mc = qe.MarkovChain(P, state_values=('unemployed', 'employed'))
mc.simulate(ts_length=4, init='employed') #初始状态：在职, 模拟未来的四个状态
>> array(['employed', 'unemployed', 'unemployed', 'unemployed'], dtype='<U10')
mc.simulate_simulate_indices(ts_length=4, init=1) 
>> array([1, 0, 0, 0])
```

- irreducible(任何两个状态都能互通eventually) 
- aperiodicity(periodic是说循环是可以预测的?)
- ergodic = aperiodic + irreducible + finite recurrence (任意取一个时间段, 所有状态都有可能出现)
- stationary: 当进行无数次迭代, 得到$\pi^*P = \pi^*$, 最终 $\pi$(正常, 衰退, 萧条) = $(0.81, 0.16, 0.02)$
$$P = \left( \begin{array}{ccc} 0.971 & 0.029 & 0 \\ 0.145 & 0.778 & 0.077 \\ 0 & 0.508 & 0.492 \end{array} \right)$$
![](~@assets/ml_math_03.png#center)

::: details 代码
```python
P = ((0.971, 0.029, 0.000),
     (0.145, 0.778, 0.077),
     (0.000, 0.508, 0.492))
P = np.array(P)

ψ = (0.0, 0.2, 0.8)        # Initial condition

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d')

ax.set(xlim=(0, 1), ylim=(0, 1), zlim=(0, 1),
       xticks=(0.25, 0.5, 0.75), xlabel='normal growth',
       yticks=(0.25, 0.5, 0.75), ylabel='mild recession',
       zticks=(0.25, 0.5, 0.75), zlabel='severe recession')

x_vals, y_vals, z_vals, colors, n = [], [], [], [], 20
for t in range(n):
    x_vals.append(ψ[0])
    y_vals.append(ψ[1])
    z_vals.append(ψ[2])
    ψ = ψ @ P

ax.scatter(x_vals, y_vals, z_vals, c='r', s=60)
ax.view_init(30, 210)

mc = qe.MarkovChain(P)
ψ_star = mc.stationary_distributions[0]
ax.scatter(ψ_star[0], ψ_star[1], ψ_star[2], cmap='cubehelix', s=60)

plt.show()
mc.stationary_distributions.round(2)
```
:::
::::
::: tab 性质

:::
:::::
::::::



## 参考

[1] 一位大神在剑桥上学期间总结的[笔记](http://dec41.user.srcf.net/), 相当全

[2] 一位北欧同学总结的统计/机器学习[笔记](https://github.com/kwichmann/statnotes)