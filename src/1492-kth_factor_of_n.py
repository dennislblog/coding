class Solution:
    """
	@问题： 给定 n = 12, k = 3 返回 n 的 第 k 个因子, 这里 n 的因子包括 [1, 2, 3, 4, 6, 12]
	@思路： 线性做法非常简单, 这里讨论 O(n^0.5)的做法，因为当2是12的因子时, 6也是, 因此直接把这个因子存下来(空间换时间)
    """
    def kthFactor(self, n: int, k: int) -> int:
    	factor = []
    	for i in range(1, math.floor(math.sqrt(n))+1):
    		if n % i == 0:
    			k -= 1
    			factor.append(n//i)
    		if k == 0:
    			return i
    	if factor[-1]**2 == n:
    		factor.pop()
    	if k > len(factor):
    		return -1
    	else:
    		return factor[-k]
        
