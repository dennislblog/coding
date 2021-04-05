---
title: 栈
date: 2021-01-03
categories:
   - Practice
tags:
   - Leetcode
---

<big> 栈：先进后出 </big>

::::: tabs type: card
:::: tab Linux路径简化
## 71. Simplify Path

__问题__： 就是给定一个路径表达式, 简化, 比如`path = "/a/./b/../../c/"`, 进过终端处理后, 得到`path = "/c"`

::: details
看到这种来来回回，增增删删的题，一般都想到用栈, 先把字符串按照`/`分割, 得到每个文件的目录名, 如果是`".."`, 就把栈顶元素出栈(如果有的话)

```python
def simplifyPath(self, path: str) -> str:
    stack = []
    for x in path.split('/'):
        if not x or x == '.':
            continue
        elif x == '..':
            if stack:  stack.pop()
        else:
            stack.append(x)
    return '/' + '/'.join(stack)
```
:::
::::
:::: tab 模拟栈
## 946. Validate Stack Sequences

__问题__： 给定`pushed`和`popped`两个序列, 判断按照`pushed`顺序, 到`popped`出来顺序, 用一个栈是否可以实现

```
输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
顺序是[4,5,3,2,1]
```

::: details
搞一个辅助栈, 模拟整个过程: 遍历入栈元素, 如果辅助栈不为空且栈顶等于出栈$[i]$, 弹出和$i+1$, 否则就加到辅助栈里
```python
def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
    stack = []; i = 0
    for num in pushed:
        stack.append(num)
        while stack and stack[-1] == popped[i]:
            stack.pop(); i += 1
    return stack == []
```
:::
::::
:::::

---

<big> 队列：先进先出 </big>
::: right
💥 按进入次序依次出栈, 和stack刚好相反
:::

::::: tip
:::: tabs type: card
::: tab 优势洗牌

## 870. Advantage Shuffle

![](~@assets/lc-870.png#right)
> - __问题__： 如何安排A的各个数字，使得对于每个位置$A[i]>B[i]$的情况最多
> - __例子__： 其实就是田忌赛马问题, 怎么安排对战顺序, 让A赢得更多

```bash
Input: A = [12,24,8,32], B = [13,25,32,11]
Output: [24,32,8,12]
```

```python
"""
- 使用双向队列, 遍历A, 每次出动自己最弱的马, i.e., `A.popleft()`
    - 如果这个马能战胜B中最弱的马(`B[0]`), 则就用这匹马对战, 
    - 否则用这匹马去斗B最强的马(`B.pop()`)
"""
def advantageCount(self, A: List[int], B: List[int]) -> List[int]:
    A = collections.deque(sorted(A))
    B = collections.deque(sorted((b,i) for i,b in enumerate(B)))
    n = len(A); res = [-1] * n
    for _ in range(n):
        a, b = A.popleft(), B[0][0]
        if a > b:
            _, i = B.popleft()
        else:
            _, i = B.pop()
        res[i] = a
    return res
```
:::
::::
:::::

---

<big> 单调栈问题 </big>

::: right
💥 维持一个单调栈, 每次弹出的元素进行一次处理, 更新结果
:::

::::: tabs type: card
:::: tab 最大柱形
## 84. Largest Rectangle in Histogram

__问题__： 给定 n 个非负整数, 例如`heights = [2,1,5,6,2,3]`，表示各个柱子的高度。每个柱子彼此相邻，且宽度为 1, 问你这里面能形成的最大柱形面积是多少

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
::::
:::: tab 接雨水
## 42. Trapping Rain Water

__问题__： 给定 n 个非负整数, 例如`heights = [0,1,0,2,1,0,1,3,2,1,2,1]`，计算按此排列的柱子，下雨之后能接多少雨水

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
::::
:::: tab 更高气温
## 739. Daily Temperatures (M)

__更高气温__: 根据每日气温 `T = [73, 74, 75, 71, 69, 72, 76, 73]`, 重新生成一个表, 对应位置的输出为：要想观测到更高的气温，还要多少天. 例如这里答案就是`[1, 1, 4, 2, 1, 1, 0, 0]`

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
::::
:::::

## 215. Kth Largest Element in an Array

::::: tip
![堆排序](~@assets/lc-heapsort.gif#right)
> - **题目**: 找到序列中第`k`大的元素, 比如 `nums = [3,2,1,5,6,4] and k = 2`
> - **要求**: 用python一行就可以搞定`heapq.nlargest(k, nums)[k-1]`, 这里要求手动实现堆排序和快排

```bash
输入: [3,2,1,5,6,4] 和 k = 2
输出: 5
```

:::: tabs type: card
::: tab 堆排序
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
::: tab 快速排序
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
![快速排序](~@assets/lc-quicksort.gif#half)
![归并排序](~@assets/lc-mergesort.gif#half)
::::
:::::

---

<big>括号问题</big>

::: right
💥 数有效的括号 + 利用栈先进后出的特点 + 还没总结完
:::

::::: tip
:::: tabs type: card
![](~@assets/lc-32.png#right)
::: tab 最长有效括号
## 32. Longest Valid Parentheses
__例子__： ")()())"的最长有效括号子串的是"()()", 长度为4
```bash
输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
```

> - 这个算法不是我自己想的, 太天才了, 先假定入栈一个')', 这样是为了区分之后'()'和')'两种情况, 前者匹配之后')'还会留在栈里, 后者直接把')'顶出去, 导致栈为空(感觉面试的时候想不出来)

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

```bash
# 动态规划, dp[i]代表以i为结尾的最长有效括号长度
# 对于"(()())"这个例子, 我们最后希望得到[0,0,2,0,4,6]

dp[i]    0   1   2   3   4   5  
add (    0   0   0   0   0   0
add (    0   0   0   0   0   0
add )    0   0   2   0   0   0         # s[i-1] = '(', 不需要往前追溯了
add (    0   0   2   0   0   0 
add )    0   0   2   0   4   0         # s[i-1] = '(', 不需要往前追溯了
add )    0   0   2   0   4   6         # s[i-1] = ')', s[i-dp[i-1]-1] = '('匹配上了
```

```python
"""
尤其注意()(())最后一个括号, 等于dp[i-1] + 2 + dp[1],不要把最后一个忘了
"""                            
def longestValidParentheses(self, s: str) -> int:
    n = len(s); dp = [0] * n
    for i, x in enumerate(s):
        if x == ')':
            if i -1 >= 0 and s[i-1] == '(':
                dp[i] = dp[i-2] + 2
            elif i-dp[i-1]-1 >= 0 and s[i-dp[i-1]-1] == '(':
                dp[i] = (0 if i-dp[i-1]-2 < 0 else dp[i-dp[i-1]-2]) + dp[i-1] + 2
    return max(dp) if dp else 0
```
:::
::: tab 括号是否有效
## 20. valid parenthesis
__例子__： "}})({{" 是无效括号, "{({})}" 是有效括号
```bash
输入：s = "}})({{"
输出：false
```

```python                            
"""没设么好说的, 模板题, 最后栈不为空
"""
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
:::
::: tab 括号得分
## 856. Score of Parentheses
__例子__： "(()(()))"返回2 x (1+2x1) = 6
```bash
输入： "(()(()))"
输出： 6
解释： ()得1分, AB得A+B分, 比如()(())是1+2分, (A)得2xA分, 比如(())是1x2
```

```python
"""
- 如果遇到`(`就往栈里面添加
- 如果遇到`)`就一直往前搜索直到栈顶元素为`(`, 把数字加起来乘以2
"""
def scoreOfParentheses(self, S: str) -> int:
    stack = []
    for s in S:
        if s == '(':
            stack.append(s)
        else:
            total = 0
            while stack and stack[-1] != '(':
                total += stack.pop()
            total = 1 if total == 0 else 2 * total 
            stack.pop(); stack.append(total)
    return sum(stack)
```
:::
::::
:::::

---

<big> 寻找子序并保存原来顺序 </big>

::: right
💥 子序列但维持原来次序 + 维持一个单调栈 + 保留多少 && 删除多少
:::

::::::: tabs type: card
::: right
凡是涉及删减, 但又必须保持原来先后次序的, 考虑使用单调栈
:::
:::::: tab 竞争力子序列
## 1673. Find the Most Competitive Subsequence
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
:::::: tab 移除K个数字
## 402. Remove K Digits
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
:::::: tab 最小非重复子序
## 1081. Smallest Subsequence of Distinct Characters
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
:::::: tab 移除重复字母
## 316. Remove Duplicate Letters 
__例子__： `nums1 = [3, 4, 6, 5], nums2 = [9, 1, 2, 5, 8, 3], k = 5`, 拼接后最大的数(长度为5)是`[9,8,6,5,3]`
- 难点在于怎么确定从`nums1`取多少个, 从`nums2`取多少个, 使得加起来等于`k`, 只想到了暴力解法, k1=0,1,2,3,4,5, k2=5-k1, 然后分别取, 最后合并
::::::
::::::: 

---

<big> 优先级队列 </big>
::: right
💥 生成`heap` + 初始化`max`和`min` + `pop min & update max`
:::

::::: tabs type: card
:::: tab 最小重叠区间
## 632. Smallest Range Covering Elements from K Lists

__例子__： 
```
nums = [ [4,10,15,24,26], 
         [0,9,12,20], 
         [5,18,22,30]
       ]
```
输出：[20,24], 最小重叠区间, 因为第一个的`24`在区间内, 第二个的`20`在区间内, 第三个的`22`在区间内
::: details
如下图所描述的那样, 维持一个三个元素的`min-heap`, 每次求这三个元素的最大最小值的差
```python
def smallestRange(self, nums: List[List[int]]) -> List[int]:
    left, right = -10**9, 10**9
    maxValue = max(x[0] for x in nums); size = [len(x) for x in nums]
    heap = [(x[0], i, 0) for i,x in enumerate(nums)]
    heapq.heapify(heap)
    while True:
        minValue, row, idx = heapq.heappop(heap)
        if maxValue - minValue < right - left:
            left, right = minValue, maxValue
        if idx == size[row] - 1:
            return [left, right]
        else:
            new_add = nums[row][idx+1]
            maxValue = max(maxValue, new_add)
            heapq.heappush(heap, (new_add, row, idx+1))
```
:::
![632. Smallest Range Covering Elements from K Lists](~@assets/lc-632.png#center)
::::
:::: tab 数组最小偏移
## 1675. Minimize Deviation in Array

__例子__： `nums = [4,1,5,20,3]`里面每一个奇数可以乘以2变成偶数, 每一个偶数可以不断除以2直到成为一个奇数, 这样我们可以把`nums`变成`nums' = [2,2,5,5,3]`这样的偏移量最小, 为最大减去最小等于`5-2=3`

我们先生成下面这个东西
```
array = [ [1,2,4],
          [1,2],
          [5,10],
          [5,10,20],
          [3,6]
        ]
```
接下来就跟前面`632`一模一样, 寻找这里面的最小重叠区间`[2,5]`, 这两个的差值就是答案
::: details
当然这里可以直接从最后一个偶数开始往前看, 每次只需要除以二即可
1. 如果本来就是偶数保存, 如果是奇数乘以二(==只能乘一次, 因为偶数只能往下除==)
2. 更新`heap`的最大最小值(重要!)
```python
def minimumDeviation(self, nums: List[int]) -> int:
    max_heap = [-x if x&1==0 else -2*x for x in nums]
    heapq.heapify(max_heap)
    res, minValue = float('inf'), -max(max_heap)
    while True:
        maxValue = -heapq.heappop(max_heap)
        res = min(res, maxValue - minValue)
        if maxValue & 1 == 1:
            return res
        else:
            new_add = maxValue>>1
            minValue = min(minValue, new_add)
            heapq.heappush(max_heap, -new_add)
    return -1
```
:::
::::
:::::