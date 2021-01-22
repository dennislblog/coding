---
title: 栈
date: 2021-01-03
categories:
   - Practice
tags:
   - Leetcode
---

## 84. Largest Rectangle in Histogram (H)
> Input: [2,1,5,6,2,3]

> Output: 10 (柱状图中最大的矩形)

::: details
给定 n 个非负整数，用来表示柱状图中各个柱子的高度，求出勾勒矩形的最大面积
- 暴力解法是遍历每一种高度，然后向两边扩散找出这个高度下的矩形面积 O(N)
- 栈就是空间换时间的做法，保证每一个元素下面是左边第一个比他矮的，而违反规则的则是右边第一个比他矮的
```python                            
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack, res = [], 0
        heights = [0] + heights + [0]
        for i, height in enumerate(heights):
            while stack and height < heights[stack[-1]]:
                cur_height = heights[stack.pop()]
                left, right = stack[-1]+1, i
                res = max(res, (right - left) * cur_height)
            stack.append(i)
        return res
```
:::

![84. Largest Rectangle in Histogram](~@assets/lc-84.png#center)


## 42. Trapping Rain Water (H)

> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]

> Output: 6 (算塘子里的积水)

::: details
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
- 暴力解法是遍历每一个元素，向左向右找到比它高的最高位置(取`min`)，减去当前高度 
- 动态规划累加 `min(max_left[i],max_right[i])−height[i]` 用两个动态数组，记录当前位置到最左和最右的高度最大值
- 用栈来跟踪可能储水的最长的条形块。 每一个元素下面是左边刚好比它高的，而违反规则的当前元素则是右边刚好比它高的
```python                            
class Solution:
    # example: [4,2,0,3,2,5]
    def trap(self, height: List[int]) -> int:
        # 单调 ↘ 单调失败, 比它小的每一个都是低, 一层层加
        stack, res = [], 0
        for i, bar in enumerate(height):
            while stack and bar >= height[stack[-1]]:
                bottom = stack.pop()
                if stack:
                    left, right = stack[-1], i
                    H = min(height[left], height[right]) - height[bottom]
                    res += (right - left - 1) * H
            stack.append(i)      # it is important to add every zeros!
        return res
```
:::

![42. Trapping Rain Water](~@assets/lc-42.gif#center)

## 739. Daily Temperatures (M)

> Input: T = [73, 74, 75, 71, 69, 72, 76, 73]

> Output: [1, 1, 4, 2, 1, 1, 0, 0] 几天后温度比今天高(每一天)

::: details
根据每日气温列表, 重新生成一个列表。对应位置的输出为：要想观测到更高的气温，至少需要等待的天数
- 暴力解法是针对每一个元素，往后遍历，直到找到第一个比它大的值，这样重复了很多步骤
- 用降序栈来跟踪温度，找到第一个不符合要求的，就是比栈顶元素温度高的
```python                            
class Solution:
    def dailyTemperatures(self, T: List[int]) -> List[int]:
        n = len(T)
        stack, res = [], [0] * n
        for i, t in enumerate(T):
            while stack and t > T[stack[-1]]:
                cur_i = stack.pop()
                res[cur_i] = i - cur_i
            stack.append(i)
        return res
```
:::

![739. Daily Temperatures](~@assets/lc-739.png#center)


## 215. Kth Largest Element in an Array

**题目**: 找到序列中第`k`大的元素, 比如 `nums = [3,2,1,5,6,4] and k = 2`

**要求**: 用python一行就可以搞定`heapq.nlargest(k, nums)[k-1]`, 这里要求手动实现堆排序和快排

::::: tabs type: card
:::: tab 堆排序
::: details
```python
def findKthLargest(self, nums: List[int], k: int) -> int:
    def heap_up(idx):
        val = minheap[idx]                       #临时存储需要上浮的元素
        while idx > 0 and minheap[(idx-1)>>1] > val:
            minheap[idx] = minheap[(idx-1)>>1]   #父节点下沉
            idx = (idx - 1) >> 1                 #index -> 父节点
        minheap[idx] = val                       #替换上浮的元素
    def heap_down(start, end):
        head_val = minheap[start]; idx = start          
        while 2*idx + 1 <= end:
            child = 2*idx + 1
            if child + 1 <= end and minheap[child] > minheap[child+1]:
                child = child + 1                #比较左右子节点, 选小的那个
            if minheap[child] < head_val:
                minheap[idx] = minheap[child]
                idx = child
            else:
                break
        minheap[idx] = head_val                  #完成节点下沉(head始终是最小)

    minheap = []
    for i in range(min(len(nums), k)):
        minheap.append(nums[i])
        heap_up(i)
    for num in nums[k:]:
        if num > minheap[0]: #heap始终保持当前最大的K个数, head是第K个
            minheap[0] = num
            heap_down(0, k-1)
    return minheap[0]
```
:::
::::
:::: tab 快速排序
::: details
``` python
def findKthLargest(self, nums, k) -> int:
    def partition(i, j):
        k = nums[i]                           #pivot,小于放左边, 大于放右边
        while i < j:
            while i < j and nums[j] >= k:     #大于pivot的不动
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]                  
            while i < j and nums[i] <= k:     #小于pivot的不动
                i += 1
            nums[j], nums[i] = nums[i], nums[j]
        return i
    n = len(nums)
    low, high = 0, n - 1
    while low <= high:
        p = partition(low, high)
        if n - p > k:                #在p这个点上, 往右n-p个元素(包括自己)
            low = p + 1              #pivot向右边移
        elif n - p < k:
            high = p - 1
        else:
            return nums[p]           #这个就是正好右边k-1个比自己大的数
    return -1
```
:::
::::
:::::

<center>
    
![快速排序](~@assets/lc-quicksort.gif#left)
![堆排序](~@assets/lc-heapsort.gif#left)
![归并排序](~@assets/lc-mergesort.gif#left)

</center>

## 括号问题

__问题__： 这种题目有很多变式, 相关的题目有`32, 最长有效括号`, `20, 判断括号是否有效` 等等

::::::: tabs type: card
:::::: tab 32. Longest Valid Parentheses
__例子__： ")()())"的最长有效括号子串的是"()()", 长度为4
::::: tabs type: card
:::: tab 栈
::: details
- 这个算法不是我自己想的, 太天才了, 先假定入栈一个')', 这样是为了区分之后'()'和')'两种情况, 前者匹配之后')'还会留在栈里, 后者直接把')'顶出去, 导致栈为空
```python                            
def longestValidParentheses(self, s: str) -> int:
    max_len = 0; stack = [-1]
    for i, x in enumerate(s):
        if x == '(':                     # now x == '('
            stack.append(i)
        else:                            # now x == ')'
            stack.pop()                  # 如果栈顶是'(', pop后栈就决不是空的
            if not stack:  
                stack.append(i)
            else:
                max_len = max(max_len, i - stack[-1])
    return max_len
```
:::
::::
:::: tab 动态规划
- 状态： dp[i]表示**以下标i为结尾**的最长有效子串的长度, 比如`(()())`, dp = [0,0,2,0,4,6]
- 状态转移方程
    1. `s[i] == '('`, 好处理, 直接为0
    2. `s[i] == ')'`, 要再分两种情况
        > `s[i-1] == '('`, 直接等于`dp[i-2]+2`<br>
        > `s[i-1] == ')'`, 那么dp[i-1]就告诉我们以i-1结尾有多少有小括号, 那么`dp[i] = dp[i-dp[i-1]-2] + dp[i-1] + 2(if s[i-dp[i-1]-1])=='('`
::: details
```python                            
def longestValidParentheses(self, s: str) -> int:
    if not s: return 0
    n = len(s); dp = [0] * n
    for i, x in enumerate(s):
        if x == '(': 
            dp[i] = 0
        else:
            if i-1 >= 0 and s[i-1] == '(':
                dp[i] = (0 if i-2<0 else dp[i-2]) + 2
            elif i-dp[i-1]-1 >= 0 and s[i-dp[i-1]-1] == '(':    #其实我觉得这个地方一定是`(`
                dp[i] = (0 if i - dp[i-1] - 2 < 0 else dp[i-dp[i-1]-2]) + dp[i-1] + 2
    return max(dp)
```
:::
::::
:::::
::::::
:::::: tab 20. valid parenthesis
__例子__： "}})({{" 是无效括号, "{({})}" 是有效括号
::::: details
```python                            
def isValid(self, s: str) -> bool:
    m_ = {")": "(", "]": "[", "}": "{"}
    stack = []
    for x in s:
        if not stack: stack.append(x)
        else:
            if x in m_ and m_[x] != stack.pop():
                return False
            elif not x in m_:
                stack.append(x)
    return not stack
```
:::::
::::::
![有效括号](~@assets/lc-32.png#center)
:::::::

## 保持顺序问题

__问题__： 像是`1673. 找出最具竞争力的子序列`这样的, 要求找出子序列, 但是子序列元素的先后次序不能改变

::::::: tabs type: card
::: right
凡是涉及删减, 但又必须保持原来先后次序的, 考虑使用单调栈
:::
:::::: tab 1673. Competitive
__例子__： `nums = [3,5,2,6], k = 2`, 中长度为2的最有竞争力子序不是`[2,3]`而是`[2,6]`因为3在2的前面
::: details
```python
def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
    n = len(nums); left = n - k
    stack = [nums[0]]
    for i in range(1,n):
        while stack and left and stack[-1] > nums[i]:
            stack.pop(); left -= 1
        stack.append(nums[i])
    return stack[:k]
```
:::
::::::
:::::: tab 402. Remove K Digits
__例子__： `nums = "1432219", k = 3`, 中去掉3个数, 得到最大子串`1219`而不是`1122`, 后者打破了原来元素之间的先后顺序
:::: details
::: danger 同上面不太一样的是这里要考虑`leading zero`的问题
```python
def removeKdigits(self, num: str, k: int) -> str:
    n = len(num); stack = []; left=n-k
    for i in range(n):
        cur = num[i]
        while stack and k and stack[-1] > cur:
            stack.pop(); k -= 1
        stack.append(cur)
    return "".join(stack[:left]).lstrip('0') or '0'
```
:::
::::
::::::
:::::: tab 1081. Smallest Distinct
__例子__： `s = "cbacdcbc"`, 最小非重复子序列是`acdb`, 而不是`abcd`, 因为`a`后面先有`c`,`d`才有`b`
:::: details
::: danger 同上面不太一样的是这里要求所有字母都得有, 且只保留第一个出现的这个字母, 次数统计的意义是避免过度删除某个字母, 导致后面不会再出现了
```python
def smallestSubsequence(self, s: str) -> str:
    remain = collections.Counter(s)          #we cannot further pop this letter if 
    n = len(s); stack = []
    for x in s:
        if not x in stack:
            while stack and stack[-1] > x and remain[stack[-1]] > 0:
                stack.pop()
            stack.append(x)
        remain[x] -= 1
    return ''.join(stack)
```
:::
::::
::::::
:::::: tab 316. Max-Number
__例子__： `nums1 = [3, 4, 6, 5], nums2 = [9, 1, 2, 5, 8, 3], k = 5`, 拼接后最大的数(长度为5)是`[9,8,6,5,3]`
- 难点在于怎么确定从`nums1`取多少个, 从`nums2`取多少个, 使得加起来等于`k`, 只想到了暴力解法, k1=0,1,2,3,4,5, k2=5-k1, 然后分别取, 最后合并
::::::
::::::: 

