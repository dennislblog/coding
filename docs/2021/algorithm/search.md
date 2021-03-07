---
title: 扫描法
date: 2021-01-02
categories:
   - Practice
tags:
   - Leetcode
---


<big> 二分法 </big>

::: right
⚙️ 预估值看能不能做出来 + 二分缩小范围
:::

:::::: tabs type: card
::::: tab 最不费力
## 1631. path with minimum effort (M)
**问题**：问你从左上角到右下角的所有路径（上下左右为valid move）哪条路径消耗的体力值最低。 **一条路径耗费的 体力值 是路径上 >相邻< 格子之间 高度差绝对值 的 最大值 决定的。** 

::: details
需要返回`j`而不是`mid`是因为`j`是能确保成功的, 而`i`和`mid`则不一定
```python
def minimumEffortPath(self, heights: List[List[int]]) -> int:

    def dfs(x, y, cap):
        if x == ncol -1 and y == nrow - 1: return True
        visited[y][x] = True  #能以cap走到最后一格才算成功
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < ncol and 0 <= ny < nrow and not visited[ny][nx] and abs(heights[ny][nx] - heights[y][x]) <= cap:
                return dfs(nx, ny, cap):
        return False

    nrow, ncol = len(heights), len(heights[0])
    dx, dy = (0,0,-1,1),(-1,1,0,0)  #上下左右
    i, j = 0, 1000000
    while i < j:
        visited = [[False] * ncol for _ in range(nrow)]
        mid = (i + j) >> 1
        if dfs(0, 0, mid):     j = mid
        else:                  i = mid + 1
    return j
```
:::
![1631. path with minimum effort](~@assets/lc-1631.png#center)
:::::
::::: tab 最小载重
## 1011. Capacity To Ship Packages Within D Days
**问题**：把一个数组按顺序输入，每天一艘船，并且每天船的承载量相同，在D天之内需要全部运出去。求每艘船的承载量最少是多少。 不能拆分 weight, 即必须一次性把 weights[i] 运出去。

**例子**：例如`weights = [1,2,3,4,5,6,7,8,9,10], D = 5`, 则最小船载重为15, 可以在5天内将货物按顺序运到

::: details
`i,j`的起始边界设置很重要, 最快可以用一个`cap=sum(weights)`的船一天拉走, 最慢可以用一个`cap=max(weights)`的慢慢拉
```python
def shipWithinDays(self, weights: List[int], D: int) -> int:

    def can_finish(cap):
        days, csum = 1, 0
        for w in weights:
            if csum + w > cap:
                csum, days = w, days + 1
            else:
                csum += w
        return days <= D

    i, j = max(weights), sum(weights)
    while i < j:
        mid = (i + j) >> 1
        if can_finish(mid):    j = mid
        else:                  i = mid + 1
    return j
```
:::
![1011. Capacity To Ship Packages Within D Days](~@assets/lc-1011.png#center)
:::::

::::: tab 分割数组
## 410. Split Array Largest Sum
**问题**：把一个非负整数数组分成`m`份, 使得各自和的最大值最小

**例子**：例如`nums=[7,2,5,10,8], m = 2`, 最好的分法是将其分为`[7,2,5]` 和 `[10,8]`, 因为这个时候各自的和分别为`14`和`18`, 答案为18, 在所有情况中最小; ==`[7,2,8`,`[5,10]`貌似更小, 但是这里切割得保持原来的次序, 所以不符合规则==

::: details
和上面那道一模一样, 就是模板题, 注意答案的上界和下界就好
```python
def splitArray(self, nums: List[int], m: int) -> int:

    def can_finish(cap):
        csum, group = 0, 1
        for num in nums:
            if csum + num > cap:   csum, group = num, group + 1
            else:                  csum += num
            if group > m:          
                return False
        return True

    i, j = max(nums), sum(nums)
    while i < j:
        mid = (i + j) >> 1
        if can_finish(mid):
            j = mid
        else:
            i = mid + 1
    return j
```
:::
![410. Split Array Largest Sum](~@assets/lc-410.png#center)
:::::

::::: tab 乘法表第K小
## 668. Kth Smallest Number in Multiplication Table
**问题**： 给定高度`m`宽度`n`的一张`m x n`的乘法表, 以及正整数`k`, 你需要返回表中第`k`小的数字。

**例子**：例如`m = 3, n = 3, k = 5`, 乘法表如下, `3x3`的表中第`k=5`小的数字是`3(因为1,2,2,3,3,4,6,6,9)`
::: details
`m x n`的乘法表, `at_least_k(x)`描述了$\text{x}$是否足够大可以成为乘法表中的$k^{th}$值, 注意每一行的数字除以行数得到的是一样的, 这个还是超时了, `test case = [9895, 28405, 100787757]`
```python
def findKthNumber(self, m: int, n: int, k: int) -> int:

    def at_least_k(x):
        cnt = 0
        for i in range(1, m+1):
            cnt += min(n, x//i)
            if cnt >= k: return True
        return False

    i, j = 1, m * n; ans = 0
    while i <= j:
        mid = (i+j) >> 1
        if at_least_k(mid):
            j -= 1; ans = mid
        else:
            i += 1
    return ans
```
:::
```
  #### 3 x 3 乘法表 #####
        1   2   3
        2   4   6
        3   6   9
```
:::::

::::: tab 最慢吃香蕉
## 875. Koko Eating Bananas
**问题**： 有 $N$ 堆香蕉, 第 $i$ 堆中有 `piles[i]` 根香蕉, 警卫已经离开了，将在 $H$ 小时后回来。 返回可以在警卫回来前吃掉所有香蕉的最小速度 $K$ (这样可以慢慢吃), 一个小时只能吃一堆香蕉且香蕉数目不能多于 $K$

**例子**：`piles = [3,6,7,11], H = 8`, 因为八小时后才回来, 如果每小时吃$K=4$颗, 那么吃掉所花时间=`sum[1,2,2,3] = 8`

::: details
这里注意`can_finish`函数中, 怎么确定一堆香蕉多少小时吃完, 比如说`pile=10`, `x=10`和`x=9`都是花费1个小时, 这个整除部分需要注意一下, 注意在二分法里`i, j`都是单向移动, 不存在`j`跳过了的情况
```python
def minEatingSpeed(self, piles: List[int], H: int) -> int:

    def can_finish(x):
        hours = 0
        for pile in piles:
            hours += (pile-1)//x + 1
            if hours > H: return False
        return True

    i, j = 1, sum(piles); ans = 0
    while i <= j:
        mid = (i+j) >> 1
        if can_finish(mid):
            j = mid - 1; ans = mid
        else:
            i = mid + 1
    return ans
```
:::
![875. Koko Eating Bananas](~@assets/lc-875.png#center)
:::::

::::: tab 最快摘花
## 1482. Minimum Number of Days to Make m Bouquets
**问题**： 返回从花园中摘 $m$ 束花需要等待的最少的天数(如果不能完成返回-1), 有一个数组`bloomDay`, 第 $i$ 朵花会在`bloomDay[i]`盛开。 注意每一束花需要从 $k$ 束盛开且相邻的花中选择

::: details
没什么好说的，和前面几道一模一样, 在`mid`天下，看盛开的花朵能不能凑够`m`束
```python
def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
    if m*k > len(bloomDay):
        return -1
    def can_finish(days):
        cnt = 0; total = 0
        for d in bloomDay:
            if d > days:  cnt = 0
            else:         cnt += 1
            if cnt == k:  
                cnt = 0; total += 1
            if total >= m: 
                return True
        return False

    i, j = 1, int(1e9); ans = -1
    while i <= j:
        mid = (i+j) >> 1
        if can_finish(mid):
            j = mid - 1; ans = mid
        else:
            i = mid + 1
    return ans
```
:::
```
假设要求 m=2 束花, 每束花需要相邻的 k=3 朵花

  #### 花第几天盛开 = [7,7,7,7,12,7,7] #### 

  第 7  天花朵盛开情况 [*,*,*,*, x,*,*] 假设 k = 3, 那么前三朵可以构成一束

  第 12 天花朵盛开情况 [0,0,0,*,*,*,*] 这个时候任意三朵相邻的都可以, 所以最少12天可以完成任务
```
:::::

::::: tab 磁力最大
## 1552. Magnetic Force Between Two Balls
**问题**：把`m`个磁球放到`n`个篮子, 第`i`个篮子的位置在`position[i]`, 怎么放可以让相互之间最小磁力最大, 磁力的定义是`f(a,b) = |pos[a] - pos[b]|`

**例子**：例如`position = [1,2,3,4,7]`, `m=3`, 最佳方案是把3个球放到`[1,4,7]`, 两两之间的磁力为`[3,3,6]`, 最小磁力为3, 其他方案最小磁力都小于3

::: details
这个地方要注意 1) 排序, 否则不好求`can_fit`; 2) 我们要的是符合`can_fit`的最大`mid`
```python
def maxDistance(self, position: List[int], m: int) -> int:

    def can_fit(force):
        pre, ball = position[0], 1
        for pos in position[1:]:
            if abs(pos - pre) >= force:
                ball += 1; pre = pos
            if ball >= m: 
                return True
        return False

    position.sort(); ans = 0
    i, j = 1, position[-1]-position[0]
    while i <= j:
        mid = (i+j) >> 1
        if can_fit(mid):
            i = mid + 1; ans = mid
        else:
            j = mid - 1
    return ans
```
::: 
![1552. Magnetic Force Between Two Balls](~@assets/lc-1552.png#center)
:::::
::::::

---

<big> 下一个排列 </big>
::::: tabs type: card
:::: tab 496
## 496. Next Greater Element III

**问题**： 给定`n=123`, 返回第一个比他大的排列, 即`n'=132`
::: details
看下面这图就明白了, 先从后往前找到一个升序, 然后和后面第一个比这个值大的调换, 然后后面翻转, ==注意`n=321`要返回`-1`而不是像31题那种返回下一种排列==
```python                            
def nextGreaterElement(self, n: int) -> int:
    
    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    nums = list(str(n)); n = len(nums); i = n-1
    while i > 0 and nums[i-1] >= nums[i]:
        i -= 1
    if i == 0: return -1
    j = n - 1
    while j >= i and nums[i-1] >= nums[j]:
        j -= 1
    nums[i-1], nums[j] = nums[j], nums[i-1]
    reverse(i, n-1)
    res = int(''.join(nums))
    return res if 1 <= res <= 2**31 - 1 else -1
```
:::
::::
:::: tab 31
## 31. Next Permutation

**问题**： 找到刚好比 `n` 大的 `permutation`. 比如 `n = 123` 输出 `132`, `n=321` 输出`123`
::: details
看下面这图就明白了, 先从后往前找到一个升序, 然后和后面第一个比这个值大的调换, 然后后面翻转
```python                            
def nextPermutation(self, nums: List[int]) -> None:

    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    n = len(nums); i = n - 1
    while i > 0 and nums[i-1] >= nums[i]:
        i -= 1
    if i - 1 >= 0:
        j = n - 1
        while j >= i and nums[i-1] >= nums[j]:
            j -= 1
        nums[i-1], nums[j] = nums[j], nums[i-1]
    reverse(i, n-1)
```
:::
::::
![496. Next Greater Element III](~@assets/lc-496.png#center)
:::::

---

<big> 排序题 </big>
::: right
⚙️ 万事不决先排序
:::

::::: tabs type: card
:::: tab 单词压缩
## 820. Short Encoding of Words
__问题__: 给你一个单词数组 words ，返回成功对 words 进行编码的最小助记字符串 s 的长度, 用`#`来标记每一个单词的结尾, 注意这里`time`和`me`共享结尾符号
```
输入：words = ["time", "me", "bell"]
输出：10
解释：一组有效编码为 s = "time#bell#" 和 indices = [0, 2, 5] 。
words[0] = "time" ，s 开始于 indices[0] = 0 到下一个 '#' 结束的子字符串，如加粗部分所示 "time#bell#"
words[1] = "me" ，s 开始于 indices[1] = 2 到下一个 '#' 结束的子字符串，如加粗部分所示 "time#bell#"
words[2] = "bell" ，s 开始于 indices[2] = 5 到下一个 '#' 结束的子字符串，如加粗部分所示 "time#bell#"
```
::: details
如果某个单词`s`能被单词`t`包含，那么它必须是`t`的后缀
- 如果`s=me`可以被压缩, 那么它必然是`t=time`的后缀, 因此只需要`time#`就可以表征两个单词, 
- 两两判断的复杂度是$O(n^2)$, 但是如果判断的单词都是大小相邻的, 就可以线性扫描比较了(按照长度和后缀的字母大小), 于是就有了下面那张图
```python
def minimumLengthEncoding(self, words: List[str]) -> int: 
    words = sorted([word[::-1] for word in set(words)]) 
    words.append("")      #！相当重要, 这样不会漏掉最后一个单词的比较
    last = ""; ans = 0 
    for word in words: 
        if not word.startswith(last): 
            ans += len(last) + 1 
        last = word return ans
```
:::
![](~@assets/lc-820.jpg#center)
::::
:::: tab 最小范围
## 910. Smallest Range II

**问题**： 在一个数列上，每一个元素`x`必须被`x+K`或者`x-K`。 问完成所有处理后, 最大值和最小值的差 最小是多少

**例子**： 比如`A = [1,3,6], K = 3`, 答案输出为3, 因为`[A[0]+3, A[1]+3, A[2]-3]`是使得最大最小差值最小的操作
::: details
就像图里描述的那样，先排好序，对于每一个点，分成两半，左边往上移(往下移会让差更大)，我们的目标是尽可能地让两段的位置差不多 (可能最高点 - 可能的最低点)
```python                            
def smallestRangeII(self, A: List[int], K: int) -> int:
    A.sort()
    n = len(A); res = A[n-1] - A[0]
    for i in range(n-1):
        mn = min(A[0]+K, A[i+1]-K)
        mx = max(A[i]+K, A[n-1]-K)
        res = min(mx - mn, res)
    return res
```
:::
![910. Smallest Range II](~@assets/lc-910.png#center)
::::
:::: tab 删除匹配
## 524. Longest Word in Dictionary through Deleting

**问题**： 从$d$中返回一个最长的匹配子字符串, 这个子字符串是$s$通过删除字符得到的

::: details
思路就是按长度降序、长度相同时字母表升序, 然后第一个能够匹配$s$删减子字符串的就是答案
```python
def findLongestWord(self, s: str, d: List[str]) -> str:
    d.sort(key=lambda x: (-len(x), x)); ns = len(s)
    for x in d:
        jx, js = 0, 0; nx = len(x)
        while jx < nx and js < ns:
            if x[jx] == s[js]:
                jx += 1; js += 1
            else:
                js += 1
        if jx == nx: return x
    return ""
```
:::
![](~@assets/lc-524.png#center)
:::: 
:::: tab 最短排序
## 581. Shortest Unsorted Continuous Subarray

__问题__： 给你一个整数数组nums=$[2,6,4,8,10,9,15]$, 找出其中最短子序列的长度, 使得只要把这个子序列排好序, 这个数组就排好了序, 在这个例子里, 只需要把$[6,4,8,10,9]$排好, 就okay了, 因此答案是5

::: details 贪心/排序法
看排好序之后, 数组左边第一个差异和最后一个差异, 这一段就是需要被排序的子序列
```python
def findUnsortedSubarray(self, nums: List[int]) -> int:
    sort = sorted(nums); n = len(nums)
    i,j = 0, n - 1
    while i < n and nums[i] == sort[i]: 
        i += 1
    while j >= i and nums[j] == sort[j]:
        j -= 1
    return j - i + 1
```
我们也可以用栈来找, 但有点多此一举, 用空间换那个整个排序的时间，左边找到第一个非升序, 用栈来找到他应该被放在的位置, 同理右边找到第一个非降序, 用栈来找到他应该被放在的位置
```python
def findUnsortedSubarray(self, nums: List[int]) -> int:
    stack = []; n = len(nums)
    l,r = n, 0
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            l = min(l, stack.pop())
        stack.append(i)
    stack = []
    for i in range(n-1, l-1, -1):
        while stack and nums[stack[-1]] < nums[i]:
            r = max(r, stack.pop())
        stack.append(i)
    return r - l + 1 if r > l else 0  #特殊情况 [1,2,3,4] 这种情况l,r都不动
```
:::
![](~@assets/lc-581.png#center)
::::
:::::

---

## 880. Decoded String at Index

**问题**： 给定一个字符串(比如`s='ha2fs2'`)，这段字符串被转录成`s'='hahafshahafs'`(数字就是重复次数的意思), 然后给定一个`K=4`, 要求你输出转录后第`K`个字符, 这里就是`a`

::: details
先扫描到第一个`size >= K`的地方，看图非常好理解
```python                            
def decodeAtIndex(self, S: str, K: int) -> str:
    size = 0 #在 s[i]之前的字母个数
    # 1. 扫描到第一个 size >= K 的位置
    for i, c in enumerate(S):
        if c.isdigit():  size *= int(c)
        else:            size += 1
        if K <= size:    break
    # 2. 对 K 取余 和 判断当下是否是数字
    while i >= 0:
        c = S[i]; K %= size
        if K == 0 and c.isalpha():  
            return c
        if c.isdigit():  size /= int(c)
        else:            size -= 1
        i -= 1
```
:::

![880. Decoded String at Index](~@assets/lc-880.png#center)

---

## 1539. Kth Missing Positive Number

**问题**： 给你一个严格升序排列正整数数组(例如`arr=[2,3,4,7]`)和一个整数(例如`k=3`), 答案应该是`6`, 因为正常排序应该是`12345678..`, 第3个缺失的数是`6`

::: details
方法1： 线性搜索, `arr[i] - (i+1)`代表当前位置前面有多少个缺失值
```python                            
def findKthPositive(self, arr: List[int], k: int) -> int:
    for i, x in enumerate(arr):
        dist = x - (i+1)
        if k <= dist:
            return x -1 - (dist - k) 
    return x + (k - dist)
```
方法2： 二分搜索，其实就是在数组排序好前提下的线性搜索
```python
def findKthPositive(self, arr: List[int], k: int) -> int:
    i, j = 0, len(arr) - 1
    while i < j:
        m = (i + j) >> 1
        if arr[m] - (m+1) >= k:  j = m 
        else:                    i = m + 1
    dif = k - (arr[i] - (i+1))
    if dif > 0:                  return arr[i] + dif
    else:                        return arr[i] - 1 + dif
```
:::

![1539. Kth Missing Positive Number](~@assets/lc-1539.png#center)

---

## 3. Longest Substring Without Repeating Characters

**问题**： 给定一个字符串(例如`s='abcdfdc'`)，请你找出其中不含有重复字符的最长子串的长度(例如这里就是`abcdf`, 答案是5)。

::: details
第一遍做的时候以为只有26个字母，结果还要考虑各种符号和数字，因此这里用上字典
- 滑动窗口，当没有重复字母的时候，移动右边界，当有重复字母的时候，移动左边界
- 这里左边界更新规则要取`max`是因为像 `pfdpppf`在遇到第二个`f`的时候，左边界不应该往后退(左边界应该一直往前走)
```python                            
def lengthOfLongestSubstring(self, s: str) -> int:
    m_ = dict(); 
    left, right, res = 0, 0, 0
    for right, cur in enumerate(s):
        if cur in m_:
            left = max(m_[cur]+1, left)
        m_[cur] = right
        res = max(res, right - left + 1)
    return res
```
:::

![3. Longest Substring Without Repeating Characters](~@assets/lc-3.png#center)

---

## 88. Merge Sorted Array

**问题**： 把两个`有序`的数组合并，把结果放到`nums1`中去。 注意这里`nums1`是有额外存储空间的, 比如`nums1 = [1,2,3,0,0,0,0]`, `nums2 = [2,5,6,8]`。 另外输入中还包括`nums1`和`nums2`初始元素个数(m=3 and n=4)

::: details
双指针, 从后往前遍历, 当 `@i2 > @i1`时, 填入`@i2`, 否则往前移动`i1`, 直到其中一个指针不能移动为止。 有一个地方要注意就是当`i1`比`i2`先走完的时候, `@i2`之前的值要复制到`nums1`里面去, 比如`nums1=[3,6,0,0] and nums2=[1,2]`这种情况, 如果不加最后一行, 返回`[3,6,3,6]`
```python                            
def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    i1, i2 = m-1, n-1
    while i1 >= 0 and i2 >= 0:
        k = i1 + i2 + 1
        if nums2[i2] > nums1[i1]:
            nums1[k] = nums2[i2]; i2 -= 1
        else:
            nums1[k] = nums1[i1]; i1 -= 1
    nums1[:i2+1] = nums2[:i2+1]
```
:::

![88. Merge Sorted Array](~@assets/lc-88.gif#center)

---

<big>两头夹逼</big>
::: right
⚙️ 排序 + 双指针从两头往中间搜索
:::

::::: tabs type: card
:::: tab 船救人
## 881. Boats to Save People

**问题**： 一条船**最多**坐两个人，同时船有个载重，问最少需要`多少条船`才能装下所有人。 

**例如**： `people=[3,2,1,2]`, 船一次最多`limit=3`, 那么需要至少三艘船才能把人都载过去

::: details
一开始想复杂了, 因为没注意一条船只能最多做两个人，其实即使允许坐多人，也应该先排序，但明显比较复杂。 但只说最多两个人就简单了，如果轻的+重的大于船载重, 让重的先坐, 因为轻的人可以和别人挤但重的不行。
```python                            
def numRescueBoats(self, people: List[int], limit: int) -> int:
    people.sort()
    i, j = 0, len(people) - 1; res = 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1
        j-= 1; res += 1
    return res
```
:::
::::
:::: tab 盛水容器
## 11. Container With Most Water
__问题__： 图中垂直线代表输入数组`height = [1,8,6,2,5,4,8,3,7]`, 求容器最多能够容纳多少水

::: details
两头夹逼, 关键是把握什么时候移动`i`什么时候移动`j`, 当宽变小的时候, 高度我们寻求更大, 因此移动的是当前较矮的那一端
```python
def maxArea(self, height: List[int]) -> int:
    i, j = 0, len(height)-1
    dist, res = j-i, 0
    while dist > 0:
        h = min(height[i], height[j])
        res = max(res, h * dist)
        if height[i] < height[j]:       i += 1
        else:                           j -= 1
        dist -= 1
    return res
```
:::
![11. Container With Most Water](~@assets/lc-11.png#center)
::::
:::::

---

## 1658. Minimum Operations to Reduce X to Zero

**问题**： 给你一个整数数组(比如`nums = [1,1,4,2,3]`)和一个整数(比如`x = 5`), 每次操作你可以从`nums`的两个边选一个数, 然后从`x`中减去该元素的值。请问最少选多少个能把`x`刚好减到`0`。 

**例子**： 比如上面这个例子里, 最少两次, 依次移除后两个元素，`x-3-2=0` 刚好为0

::::: details
:::: tabs type: card
::: tab 分段求和
这其实就是个求和问题, :one: 全在左边; :two: 全在右边; :three: 两个交叉
```python
def minOperations(self, nums: List[int], x: int) -> int:
    left, right = {}, {}
    n = len(nums) - 1; res = 0
    total = 0 
    for i in range(nums):
        total += nums[i]; left[total] = i+1
    total = 0
    for i in range(nums):
        total += nums[n-i]; right[total] = i+1
    res = min(left.get(x, float('inf')),right.get(x, float('inf')))
    for key in left:
        if x - key in right:
            res = min(res, left[key] + right[x-key])
    return -1 if res == float('inf') else res
```
:::
::: tab 滑动窗口
用滑动窗口的办法, 要求外部最短, 即找中间最大, 可以参考[这道题](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/)。 找到中间(包括左右闭区间)最长的一段, 使得和等于`total - x`
```python
def minOperations(self, nums: List[int], x: int) -> int:
    i, j = 0, 0 #sliding window left and right idx
    total, maxLen, n, target = 0, -1, len(nums), sum(nums) - x
    while i < n:
        while j < n and total < target:
            total += nums[j]; j += 1
        if total == target:
            maxLen = max(maxLen, j-i)
        total -= nums[i]; i += 1
    return n - maxLen if maxLen != -1 else -1
```
:::
::::
:::::