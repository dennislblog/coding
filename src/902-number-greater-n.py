from typing import List


class Solution:
    """
        @问题： digits = ["1","3","5","7"], n = 100, 我们需要从digits里找出所有比100小的数字组合(可以重复)
        @思路： 
            - 看 n 的位数，这里是3位数，那至少 xx 两位数 和 x一位数的都满足，关键是遇到当前位 = 【1，3，5，7】的情况
            - 什么时候不用再往下看了呢？就是没有出现当前位 = [1，3，5，7】的情况
        ------------------------------------------------------------------
        比如 digits = [1,3,5,7] and N = 554 
        -----------------------------------
        i = 1            res += 4  (x)
        i = 2            res += 16 (xx)
        -----  现在开始看最高位  -------
        i = 0            res += 16*2 (1xx 和 3xx)
        -----  继续循环因为当前位 5 在 [1,3,5,7] ----
        i = 1            res +=  4*2 (51x 和 53x)
        i = 2            res +=  1*2 (551 和 553)
        -----  直接 return res 因为 N 的最后一位不在 [1,3,5,7] 里
    """
    def atMostNGivenDigitSet(self, D: List[str], N: int) -> int:
        # each d in D in '1' -> '9'; D is sorted; 1 <= N <= 1e9
        N = str(N)
        nN, nD = len(N), len(D)
        res = 0
        for i in range(1, nN):
            res += nD ** i
        for i in range(nN):
            curN = N[i]
            for d in D:
                if d < curN:
                    res += nD ** (nN - 1 - i)
                else:
                    break
            if not curN in D:
                return res
        return res + 1  # add itself when every number is in D
