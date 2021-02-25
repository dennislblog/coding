---
title: 动态规划
date: 2021-01-14
categories:
   - Practice
tags:
   - Leetcode
---

## 413. Arithmetic Slices
__问题__： 找出一个数组有多少个等差数列(至少三个数)

__例子__： $A = [1, 2, 3, 4]$, 有`[1,2,3]; [2,3,4]; [1,2,3,4]`四个等差数列，数列必须是连续数字，如果允许非连续会难很多

::: details
首先如果暴力破解的话
- 找一个开头`s`, 找一个结尾`e=s+2`, 看$A[s+1]-A[s]==A[s+2]-A[s+1]$如果可以构成等差数列, 就继续往右挪动$e$, 代表可以以$s$为起点创建长度更长的等差数列
- 一旦不行, 就停止挪动$e$, 转而用新的起始点$s$去找新的`difference`

用动态规划, 生成下面这样的东西, 其实就是形成等差数列后移动右边的点, 然后左边从右边断开的点开始重新走(而不是从上一个起始点+1开始看)

```python     
"""注意动态规划可以进一步优化空间, 因为dp[i]只和dp[i-1]有关系
A   1  3  5  7  9 15 20 25 28 29
dp  0  0  1  2  3  0  0  1  0  0
"""                       
def numberOfArithmeticSlices(self, A: List[int]) -> int:
    n = len(A); dp = [0] * n; res = 0
    for i in range(2,n):
        if A[i-1]*2 == A[i]+A[i-2]:
            dp[i] = dp[i-1] + 1
        else:
            dp[i] = 0
    return sum(dp)
```
:::

![413. Arithmetic Slices](~@assets/lc-413.png#center)

## 1105. Filling Bookcase Shelves

__问题__： 要求把书(不同厚度和高度)按照顺序放在一个书柜里(分层), 这个书架是有固定宽度的, 但是可以不断加层。

__例子__： books(宽度,高度) = $[[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]]$, shelf_width = $4$, 见下图

::: details
用动态规划作, 设$d[i]$为放置前$i$本书的最小高度, 把当前这本书尽量放在同一层, 如果超了书柜的宽度, 则加一层, ==但是要注意上一层的书也许应该放下来最好, 因为这一层目前只有一本书==

```python
"""
dp[i] 的范围注意一下, 最多1000本书, 最高1000, 所以dp[i]的最大值
这道题用二分法也不好做, 原因就是图中的那个, 即使有高度限制, 怎么放还是有trick
"""
def minHeightShelves(self, books: List[List[int]], shelf_width: int) -> int:
    n = len(books); dp = [1000000] * (n+1); dp[0] = 0
    for i, book in enumerate(books):
        add_w = 0; max_h = 0
        for j in range(i, -1, -1):
            add_w += books[j][0]
            if add_w > shelf_width:
                break
            max_h = max(max_h, books[j][1])                
            dp[i+1] = min(dp[i+1], dp[j] + max_h)
    return dp[-1]
```
:::

![](~@assets/lc-1105.png#center)