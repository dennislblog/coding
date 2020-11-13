class Solution:
    """
        @example: [6,-7,5,-3,1]
        @solution: 因为有环，所以不能只考虑最大子序，还要考虑最小子序，有下面这四种情况
                   - 最大子序在环上,   max_sum = total_sum - min_sum (1)
                   - 最大子序不在环上, max_sum = max_sum             (2)
                   所以我们只需要比较(1)和(2)，但是有可能所有数字都是负数，这种情况下，(1) = 0, (2) < 0
        -----------------------------------------------------------------------------------------
            pointer         6       -7      5       -3      1
            max_(local)     6       -1      5        2      3
            mx              6        6      6        6      6
            min_(local)     6       -7     -2       -5     -4
            mn              6       -7     -7       -7     -7
            -------------------------------------------------
            output    max(2 - (-7), 6)
    """
    def maxSubarraySumCircular(self, A: List[int]) -> int:
        mn, mx = float('inf'), float('-inf')
        max_, min_, sum_ = 0, 0, 0
        for a in A:
            max_ = max(max_+ a, a)
            mx = max(mx, max_)
            min_ = min(min_+a, a)
            mn = min(mn, min_)
            sum_ += a
        if sum_ == mn:
            return mx
        else:
            return max(sum_ - mn, mx)