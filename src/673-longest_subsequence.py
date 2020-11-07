class Solution(object):
    def findNumberOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        @ 问题：number of longest increasing subsequences.

            @ solution: 创建两个DP，size[i] := 到[i]为止的最长子序长度， cnt[i] := 最长子序的个数
            @ example: [1,3,5,4,7]  ==> return 2 最长子序长度为4，有两个[1, 3, 4, 7]和[1, 3, 5, 7]
            ------------------------------------------------------------------------------------
            i                size                           cnt
            0                [1, 1, 1, 1, 1]                [1, 1, 1, 1, 1]
            1                [1, 2, 1, 1, 1]                [1, 1, 1, 1, 1]
            2                [1, 2, 3, 1, 1]                [1, 1, 1, 1, 1]
            3                [1, 2, 3, 3, 1]                [1, 1, 1, 1, 1] (1354 最长还是134)
            4                [1, 2, 3, 3, 4]                [1, 1, 1, 1, 2] 
        """
        n = len(nums)
        size, cnt = [1] * n, [1] * n
        max_size, max_cnt = 0, 0
        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:
                    if size[i] == size[j] + 1:
                        cnt[i] += cnt[j]
                    #当 size[i] 比 size[j]+1 更大时，加入nums[i] 并不促成最长子序
                    elif size[i] < size[j] + 1: 
                        size[i] = size[j] + 1
                        cnt[i] = cnt[j]
            if size[i] > max_size:
                max_size = size[i]
                max_cnt = cnt[i]
            elif size[i] == max_size:
                max_cnt += cnt[i]
        return max_cnt