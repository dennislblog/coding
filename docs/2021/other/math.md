---
title: 数学知识
date: 2021-02-04
autoGroup-3: 知识 
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