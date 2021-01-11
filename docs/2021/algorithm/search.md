---
title: 扫描法
date: 2021-01-02
categories:
   - Practice
tags:
   - Leetcode
---

## 1011. Capacity To Ship Packages Within D Days
> Input: weights = [1,2,3,4,5,6,7,8,9,10], D = 5

> Output: 以 15 作为载重的船，可以在 5 天内将货物运到

**问题**：把一个数组按顺序输入，每天一艘船，并且每天船的承载量相同，在D天之内需要全部运出去。求每艘船的承载量最少是多少。 不能拆分 weight, 即必须一次性把 weights[i] 运出去。
::: details
二分搜索, 找到最大的 `cap` 使得在 D 天内可以运到 (即 `shipWithinDays(cap) <= D`)
```python                            
"""
    @day_when_capacity 返回以 cap 为大小的船，最短几天可以完成目标
"""
def shipWithinDays(self, weights: List[int], D: int) -> int:
    
    def day_when_capacity(cap):
        days, csum = 1, 0
        for w in weights:
            if csum + w > cap:
                csum, days = w, days + 1
            else:
                csum += w
        return days
    
    low, high = 0, 0
    for w in weights:
        low = max(low, w)
        high += w
    
    res = high                 #initialize answer to be max capacity
    while low < high:
        mid = (low + high) >> 1
        day = day_when_capacity(mid)
        if day > D:
            low = mid + 1
        else:                   #all res in this category satisfy d < D, find minimum
            high = mid
            res  = min(res, mid)
    return res
```
:::

![1011. Capacity To Ship Packages Within D Days](~@assets/lc-1011.png#center)


## 496. Next Greater Element III

**问题**： 找到刚好比 `n` 大的 `permutation` 如果没有(比如987654)则返回 -1

**例子**： 比如 `n = 123` 输出 `132`
::: details
翻转的技巧，从后往前找到第一个拐点(比如图中的`4`), 然后翻转后面得到以`4`开头最小的数字, 然后用里面刚好比`4`大的数字(比如这里的`6`)去替换
```python                            
def nextGreaterElement(self, n: int) -> int:
    
    def reverse(l, r):
        while l < r:
            num[l], num[r] = num[r], num[l]
            l += 1
            r -= 1
    
    num = list(str(n)); i = j = len(num) - 1
    while i > 0 and num[i-1] >= num[i]:
        i -= 1
    if i == 0: return -1
    reverse(i, j)
    for k in range(i, j+1):
        if num[k] > num[i-1]:
            num[k], num[i-1] = num[i-1], num[k]
            break
    res = int(''.join(num))
    return res if 1 <= res <= 2**31 - 1 else -1
```
:::

![496. Next Greater Element III](~@assets/lc-496.png#center)


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
