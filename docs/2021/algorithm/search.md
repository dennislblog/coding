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
class Solution:
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

