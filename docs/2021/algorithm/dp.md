---
title: 动态规划
date: 2021-01-14
categories:
   - Practice
tags:
   - Leetcode
---


<big>股票问题</big>
::: right
📦 怎么尽可能在有限空间的背包里尽可能多地装货
- 121
- 123
- 309
- 122
- 188
- 714
:::

定义一个三维数组, `dp[i][j][k]`代表第`i`天第`j`次交易(先买再卖算一次), 最后手里是否持有股票`k`所持有的总利润
```
dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j-1][0] - prices[i])
```
- 第$i$天我没有持有股票, 要么是我昨天就没有持有, 今天继续闲着; 要么是我昨天持有股票, 今天卖掉, 所以我今天没有持有股票了
- 第$i$天我持有股票, 要么我昨天就持有着股票, 今天继续闲着; 要么是我昨天没有持有股票, 今天买入一股, 今天才持有股票

::::: tabs type: card
:::: tab 最佳时机 I
## 121. Best Time to Buy and Sell Stock
__问题__： 可以在某一天购入一股, 之后卖掉, 求最大收益
```
Input: [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
```
::: details
```
因为只能进行一次交易, 因为dp[n][0][0] = 0(一次交易没发生, 且没有购买行为),
所以状态转移同交易次数无关

dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i]) 
            = max(dp[i-1][1], 0-prices[i])       
```
同样我们发现状态转移只和昨天是否持有股票有关系, 因而可以进一步用两个变量来代替数组
```python
"""其实直接用当前数字减去之前遇到的最小数字即可
dp0: 此刻手里没有股票的最大收益
dp1: 此刻手里有股票的最大收益
"""
def maxProfit(self, prices: List[int]) -> int:
    dp0, dp1 = 0, -float('inf')
    for price in prices:
        dp0 = max(dp0, dp1+price)
        dp1 = max(dp1, -price)
    return dp0
```
:::
::::
:::: tab 最佳时机 II
## 122.Best Time to Buy and Sell Stock II 
__问题__： 可以进行多次交易
```
Input: [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4. 
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
```
::: details
```
在这道题中, k是正无穷的, 那么就可以认为 k 和 k - 1 是一样的, 因此第二个维度没意义

dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i]) 
```
同样我们发现状态转移只和昨天是否持有股票有关系, 因而可以进一步用两个变量来代替数组, 但是在更新第二个变量的时候用的是第一个变量更新前的结果
```python
def maxProfit(self, prices: List[int]) -> int:
    dp0, dp1 = 0, -float('inf')
    for price in prices:
        old_dp0 = dp0
        dp0 = max(dp0, dp1+price)
        dp1 = max(dp1, old_dp0-price)
    return dp0
```
:::
::::
:::: tab 最佳时机 III
## 123. Best Time to Buy and Sell Stock III
__问题__： 最多两次交易
```
Input: [3,3,5,0,0,3,1,4]
Output: 6
Explanation: Buy on day 4 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3. 
Then buy on day 7 (price = 1) and sell on day 8 (price = 4), profit = 4-1 = 3.
You can only do 2 trades !
```
::: details
```
在这道题中, 交易次数有限制并且 j = 2, 所以要考虑第二个维度(穷举k=2,k=1次交易的情况)

dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j-1][0] - prices[i]) 
```
用二维数组避免出错, 主要就是注意一下买的时候, 是否已经超过两次交易了, 然后状态更新的顺序从后往前
```python
def maxProfit(self, prices: List[int]) -> int:
    # dp: time x trade
    dp0 = [[0]*3 for _ in range(2)]
    dp1 = [[-float('inf')]*3 for _ in range(2)]
    for price in prices:
        for j in range(2,0,-1):
            dp0[1][j] = max(dp0[0][j], dp1[0][j]+price)
            dp1[1][j] = max(dp1[0][j], dp0[0][j-1]-price)
            dp0[0][j],dp1[0][j] = dp0[1][j],dp1[1][j]
    return dp0[1][2]
```
:::
::::
:::: tab 最佳时机 IV
__问题__： 最多$k$次交易
```
Input: [2,4,1], k = 2
Output: 2
Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.
```
::: details
和上面那道题的模板一模一样, 只是要注意有个special case, $K$的值非常大, 导致内存超出, 解决的办法就是加约束条件： $K \leq N/2$, 因为每次交易要至少两个阶段才能完成
```python
def maxProfit(self, k: int, prices: List[int]) -> int:
    if not prices: return 0
    n = len(prices); max_k = min(k, n//2)
    dp = [[[0]*2 for _ in range(max_k+1)] for _ in range(n)]
    for i in range(n):
        for k in range(max_k, 0, -1):
            if i == 0:       #特殊情况处理一下
                dp[i-1][k][1] = -float('inf')   
            dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
            dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])
    return dp[-1][-1][0]
```
:::
::::
:::: tab 最佳时机 V
## 309. Best Time to Buy and Sell Stock with Cooldown
__问题__： 在买入之前必须至少休息一天, 还是无限交易次数
```
Input: [7,1,5,1,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit =6-1 = 5. 
cannot sell on day 3 and buy again on day 4
```
::: details
```
在这道题中, 交易次数无限制, 所以第二个维度还是没有意义
然后cooldown的话, 限制了买入行为, 即必须从dp[i-2][0]那里获得之前无持有状态的最佳利润

dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], dp[i-2][0] - prices[i]) 
```
无持有必须保存$t-1$和$t-2$的信息, 而持有仅须保存$t-1$的信息
```python
"""比如 input = [1,2,3,0,2]

>> p=1      dp0=[0,0,0]     dp1=-1       
>> p=2      dp0=[0,0,1]     dp1=-1
>> p=3      dp0=[0,1,2]     dp1=-1    每次把dp0[1,2]搬运到dp0[0,1]
>> p=0      dp0=[1,2,2]     dp1= 1
>> p=2      dp0=[2,2,?]     dp1= 1    ?=3, 因为第1,2天完成一次, 第4天已经可以继续买了
"""
def maxProfit(self, prices: List[int]) -> int:
    dp0 = [0] * 3
    dp1 = -float('inf')
    for i, price in enumerate(prices):
        dp0[1], dp0[0] = dp0[2], dp0[1]
        dp0[2] = max(dp0[1], dp1 + price)
        dp1 = max(dp1, dp0[0] - price)
    return dp0[-1]
```
:::
::::
:::: tab 最佳时机 VI
## 714. Best Time to Buy and Sell Stock with Transaction Fee
__问题__： 没有冷冻期, 但是每次交易都要交一个手续费
```
Input: [1,2,4,0,2], fee=2
Output: 1
Explanation: Buy on day 1 and sell on day 3, get profit of 1
```
::: details
```
在这道题中, 交易次数无限制, 所以第二个维度还是没有意义
有手续费相当于卖的时候多交一笔钱, 注意fee加到上面会存在dp1不能再减小的问题

dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i]-fee) 
```
用两个变量来代替数组, 在更新第二个变量的时候用的是第一个变量更新前的结果
```python
def maxProfit(self, prices: List[int], fee: int) -> int:
    dp0, dp1 = 0, -float('inf')
    for price in prices:
        old_dp0 = dp0
        dp0 = max(dp0, dp1+price)
        dp1 = max(dp1, old_dp0 - price - fee)
    return dp0
```
:::
::::
:::::

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



