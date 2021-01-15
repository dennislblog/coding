---
title: 动态规划
date: 2021-01-14
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

