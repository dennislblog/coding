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