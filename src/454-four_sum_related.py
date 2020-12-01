class Solution:
    """
        @问题： 给定四个序列 A,B,C,D; 求有多少个 a+b+c+d = 0 
        @思路： 碰到求和问题，优先考虑hash-map，把A和B的两两之和都求出来，然后找-(c+d)的映射 
    """
    def fourSumCount(self, A: List[int], B: List[int], C: List[int], D: List[int]) -> int:
        cnt1, cnt2 = dict(), dict()
        for a in A:
            for b in B:
                cnt1[a+b] = cnt1.get(a+b, 0) + 1
        res = 0
        for c in C:
            for d in D:
                target = -(c+d)
                res += cnt1.get(target, 0)
        return res
        