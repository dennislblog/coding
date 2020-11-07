class Solution(object):
    def singleNonDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        @问题：sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.
        
            @ example: [1,1,2,3,3,4,4,8,8]  ==> 找到 2
            -------------------------------------
            # of run    i     j     nums[(i+j)/2]
            1st         0     8                 3
            2nd         0     3                 1
            3rd         1     3                 2(左右两边都不等)
        """
        # 如果是O(n)就直接用xor解决了，这里要求二分法求解
        # 利用中点的index，比较左右两边的数，看唯一落单的那个会是在哪一边
        i, j = 0, len(nums) - 1
        while i < j:
            k = (i+j) >> 1
            cur = nums[k]
            # 1. 左右各奇数个
            if k % 2:
                # 1.1 右边相同，在左边
                if nums[k+1] == cur:
                    j = k
                # 1.2 左边相同，在右边
                elif k > 0 and nums[k-1] == cur:
                    i = k + 1
                else:
                    return cur
            # 2. 左右各偶数个
            else:
                # 2.1 右边相同，在右边
                if nums[k+1] == cur:
                    i = k + 1
                # 1.2 左边相同，在左边
                elif k> 0 and nums[k-1] == cur:
                    j = k
                else:
                    return cur
        return nums[i]
