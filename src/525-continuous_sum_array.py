class Solution:
	"""
	@问题： 从 nums = [0,1,0,0,1] 中找出最长子串（0和1的数目相等）
	@思路： 用做差的思想, 如果每碰到1次0，计数器加1，碰到一次1，计数器减1
				- 如果 A[i] = A[j] 那么 A[i+1:j] 一定等于0 (*)
				- 把 j - i 和 res 比较长度
	@例子： nums = [0,1,0,0,1]
	-------------------------------------
	
	"""
    def findMaxLength(self, nums: List[int]) -> int:
        cnt = {0: -1}
        res, total = 0, 0
        for i, num in enumerate(nums):
        	if num == 1: total += 1
	        else:        total -= 1
	        if total in cnt:
	        	res = max(i - cnt[total], res)
	        else:
	        	cnt[total] = i
	    return res

    """
	@相关： 325题 Maximum Size Subarray Sum Equals k 最大子数组之和为k
	@例子： nums = [1, -1, 5, -2, 3], k = 3  ==> 返回4因为[1, -1, 5, -2] is subarray with sum=k
	@思路： 和这道题一模一样的做法，记录total sum
    """
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
    	cnt = {0: -1}
    	res, total = 0, 0
    	for i, num in enumerate(nums):
    		total += num
    		if total - k in cnt:
    			res = max(res, i - cnt[total-k])
    		if not total in cnt:
    			cnt[total] = i
    	return res

