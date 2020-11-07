class Solution(object):
    def find132pattern(self, nums):
        """
        :type nums: List[int]
        :rtype: bool

            @ solution: 先匹配 $3$2 最好在匹配 $1$3$2 
            @ example: nums = [-1,3,2,0] ==> return True (-1 -> 3 -> 2 是 132 pattern)
            -------------------------------------------------------------------------
            i              nums[i]            stack             third
            3                    0               [0]             -inf
            2                    2               [2]                0 (有了32pattern了，$3=cur, $2=stack.pop()最近的一次)
            1                    3               [3]                2 (现在只要再找到一个比$2小的数就完成了寻找)
        """
        n = len(nums)
        if n < 3: return False
        third = float('-inf')
        stack = []
        for i in range(n-1, -1, -1):
            cur = nums[i]
            if cur < third:
                return True
            while stack and stack[-1] < cur:
                third = stack.pop()
                # now we have '32', just find '1'
            stack.append(cur)
        return False