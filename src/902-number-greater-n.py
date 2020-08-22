from typing import List


class Solution:
    def atMostNGivenDigitSet(self, D: List[str], N: int) -> int:
        # each d in D in '1' -> '9'; D is sorted; 1 <= N <= 1e9
        # 0. for example, the number is 5 x x x
        N = str(N)
        nN, nD = len(N), len(D)
        res = 0
        # 1. forget about first digit, x x x
        for i in range(1, nN):
            res += nD ** i
        # 2. first digit consideration, ? x x x 只检查最高位，如果相等才往下查
        # 2.1 if ? in D, continue to examine the next digit until d != digit
        # 2.2 otherwise, keep adding d x x x where d < digit
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
