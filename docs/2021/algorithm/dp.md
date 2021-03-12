---
title: 动态规划
date: 2021-01-14
categories:
   - Practice
tags:
   - Leetcode
---


<big>背包问题</big>
::: right
📦 怎么尽可能在有限空间的背包里尽可能多地装货
- 473
- 474
- 279
:::

::::: tabs type: card
:::: tab 零钱兑换
## 322. Coin Change
__问题__: 用最少的硬币凑齐领钱(amount)

__例子__: 比如 "coins = [1, 2, 5], amount = 11" 最少三枚硬币就可以搞定, 如果搞不定返回`-1`

```coins = [2,5,1]
dp[i]    0   1   2   3   4   5   6   7   8   9  10  11
add 2    0  12   1  12   2  12   3  12   4  12   5  12
add 5    0  12   1  12   2   1   3   2   4   3   2  12
add 1    0   1   1   2   2   3   2   2   3   3   2   3
```
::: details 
动态规划, 清晰明了, 见下图
```python
def coinChange(self, coins: List[int], amount: int) -> int:
    dp = [amount+1] * (amount + 1); dp[0] = 0
    for coin in coins:
        for i in range(coin, amount+1):
            dp[i] = min(dp[i], dp[i-coin]+1)
    return -1 if dp[-1] == amount+1 else dp[-1] 
```
:::
::::
:::: tab 零钱兑换二
## 518. Coin Change 2
__问题__： 和上面那道题差不多, 只是问你要凑够`amount`, 用手里这堆硬币, 总共有多少种不同组合方式

__例子__： 比如之前那个例子总共有11种方式

```coins = [2,5,1]
dp[i]    0   1   2   3   4   5   6   7   8   9  10  11
add 2    1   0   1   0   1   0   1   0   1   0   1   0
add 5    1   0   1   0   1   1   1   1   1   1   2   0
add 1    1   1   2   2   3   4   6   7   8   9  11  11
```
::: details
下面两个相加即可
- 还没更新的`dp[i]`代表不add当前这个coin时的答案
- `dp[i-coin]`代表答案中必须包含当前这个coin的答案个数
```python
def change(self, amount: int, coins: List[int]) -> int:
    dp = [0] * (amount + 1); dp[0] = 1
    for coin in coins:
        for i in range(coin, amount+1):
            dp[i] += dp[i-coin]
    return dp[-1]
```
:::
::::
:::: tab 分割两半
## 416. Partition Equal Subset Sum

__问题__： 判断是否可以把一组数字分成两堆，两堆数字的和相等

__例子__： "[1, 2, 3, 8]", 不可以分成相等的两堆

```nums=[3, 1, 2, 8]
dp[i]    0   1   2   3   4   5   6   7
add 3    T   F   F   T   F   F   F   F 
add 1    T   T   F   T   T   F   F   F 
add 2    T   T   T   T   T   T   T   F 
```

::: details
总和除以2是背包的负载, 我们只需要一个一个往里更新, 要从后往前更新, 因为数字不能重复被使用, 就
- `dp[i]`代表不加当前`num`情况下, `total=i`是否凑得齐
- `dp[i-num]`代表这一堆里一定包含当前`num`的情况下, `total=i`是否凑得齐
```python
def canPartition(self, nums: List[int]) -> bool:
    target = sum(nums)
    if target % 2 == 1: return False
    target = target >> 1
    dp = [False] * (target + 1); dp[0] = True
    for num in nums:
        for i in range(target, num-1, -1):
            dp[i] |= dp[i-num]
    return dp[-1]
```
:::
::::
:::: tab 目标和
## 494. Target Sum
__问题__： 给定一个数组, 每一个数字前面可以加＋或者－, 然后加起来要等于一个给定的数字, 请问有多少种不同的assignment(这些符号)

__例子__： `nums=[1, 1, 1, 1, 1], S=3`, 一共有5种, 其实就是"(sum(nums)-S) / 2"作为背包的负载, 然后看有多少个加和可能

::: details
也是保持从后往前更新, 因为一个数字只能使用一次
```python
def findTargetSumWays(self, nums: List[int], S: int) -> int:
    target = sum(nums) - S
    if target % 2 == 1 or target < 0: return 0
    target = target >> 1
    dp = [0] * (target + 1); dp[0] = 1
    for num in nums:
        for i in range(target, num-1, -1):
            dp[i] += dp[i-num]
    return dp[-1] or 0
```
:::
::::
:::: tab 暂无

::::
:::::

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


## 1246. Palindrome Removal 

__问题__： 每次可以删除一个回文子数组(不是子字符串, 就是说必须是邻近的才可以), 问多少次可以删除干净

__例子__： "arr = [1,3,4,1,5]", 先先删除 "[4]", 然后删除 "[1,3,1]", 最后再删除 "[5]"

::: details
主要是考虑"arr[i, j]"需要多少步, 如果$i=j$, 我们可以直接考虑"arr[i+1, j-1]"但也不一定, 因为有可能$i$是和前面的某些字符串已经组成了`palindrome`, 所以才有倒数第二步. 
```python
def minimumMoves(self, A: List[int]) -> int:
    N = len(A); dp = [[0] * N for _ in range(N)]

    def helper(i=0, j=N-1):
        if j < i:  return 0
        if j == i: return 1
        if dp[i][j] != 0: return dp[i][j]
        res, tmp = float('inf'), 0
        for k in range(i+1, j):
            if A[i] == A[k]:
                if k == i + 1:  #they are right next to each other
                    tmp = 1 + helper(k+1, j)
                else:
                    tmp = helper(i+1, k-1) + helper(k+1, j)
                res = min(res, tmp)
        dp[i][j] = res = min(res, 1 + helper(i+1, j))
        return res
    
    return helper()
```
:::

![](~@assets/lc-1246.png#center)