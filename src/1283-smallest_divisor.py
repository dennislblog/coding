class Solution(object):
    def smallestDivisor(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        @ 问题： Find the smallest divisor such that the result mentioned above <= threshold.

            @ example: [1,2,5,9], threshold = 6 ==> return 5 because 1/5 + 2/5 + 5/5 + 9/5 = 5 < 6
            --------------------------------------------------------------------------------------
            i                          j                    sum(i+j)/2
            1                          16                   sum(8) = 5 <= 6
            1                          8                    sum(4) = 7 >  6
            5                          8                    sum(6) = 5 <= 6
            5                          5                    return i=j=5
        """
        # 1. 二分求最适合的divisor, 在1 - 1e6之间
        # 2. 如果得到的结果比threshold小(一开始), 再继续尝试更小的除数
        def sum(divisor):
            total = 0
            for n in nums:
                total += (n+divisor-1)//divisor
            return total
        i, j = 1, 1000000
        res = 0
        while i < j:
            k = (i+j) >> 1
            if sum(k) <= threshold:
                j = k
            else:
                i = k + 1
        return i