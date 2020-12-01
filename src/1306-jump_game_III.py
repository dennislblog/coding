class Solution:
	"""
	这种类型的题目总共3道，分别是55, 45 和这一道, 先来看最难的这道题

	@问题： 给定 nums = [4,2,3,0,3,1,2] 
				每一个index 你下一个能到达的位置，比如在 i=5的地方 value=1 代表可以往前或往后移动一个位置
				start=5代表最开始的位置，问能不能通过移动到达 value = 0 的位置
	@例子： 
		Input : arr = [4,2,3,0,3,1,2], start = 5
		Output: true
		Why   : index 5 (v=1) -> index 4 (v=3) -> index 1 (v=2) -> index 3 (v=0)
	@思路： 这道题和前面两道不太一样，because 每次只有两个固定的位置可以跳
								   所以 BFS/DFS游历是最好的，当 val = 0 返回True

	"""
    def canReach(self, arr: List[int], start: int) -> bool:
    	# 1. BFS
    	n = len(arr)
        visited, queue = [0] * n, deque([start])
        while queue:
            cur = queue.popleft()
            visited[cur] = 1
            if arr[cur] == 0:
                return True
            for ncur in [cur-arr[cur], cur+arr[cur]]:
                if 0 <= ncur <= n-1 and not visited[ncur]:
                    queue.append(ncur)
        return False

    def canReach(self, arr: List[int], start: int) -> bool:
        # 2. DFS
        n = len(arr)
        visited = [0] * n
        def dfs(cur):
            if cur < 0 or cur > n-1 or visited[cur]:
                return False
            visited[cur] = 1
            if arr[cur] == 0:
                return True
            return dfs(cur+arr[cur]) | dfs(cur-arr[cur])
        return dfs(start)

    """
	@55题： 给定 nums = [2,2,1,0,4], 每一个index代表能跳跃的最大距离, 问能不能跳到最后一个index
	@45题： 给定 nums = [2,3,1,1,4], 每一个index代表能跳跃的最大距离, 最短多少步能够到最后一个

	@思路： 这两道题都可以用贪心算法(和动态规划不同，虽然都是局部最优->全局最优, 
			在动态规划中，全局最优解中一定包含之前某一个DP状态，因此需要记录所有状态
			而贪心策略中，每一步的最优解一定包含上一步的最优解)
    """
    def canJump(self, nums: List[int]) -> bool:
    	"""
		Input : nums = [2,2,1,0,4]
		Output: False
    	Why   : the 3rd has value zero, which stops me to get last position

    	记录能达到的最远位置, 依次往右移动，如果当前光标 > 最远位置，代表这个地方去不了，返回False
    	-----------------------------------------------------------------------------------
    	i = 0 	reach = 2
    	i = 1   reach = 3 (下一步最远可以达到index=3)
    	i = 2   reach = 3
    	i = 3   reach = 3 
    	i = 4   reach = 3 (返回 false 因为 reach < i) 之所以不是 reach <= i 是因为万一 reach 恰好等于 last index?
    	"""
    	reach = 0
    	for i, num in enumerate(nums):
    		if reach < i:  #不要先更新reach
    			return False
    		reach = max(reach, i+num)
    	return True
    	
    def canJump(self, nums: List[int]) -> bool:
    	"""
		Input : nums = [2,3,1,1,4,2]
		Output: 2
    	Why   : 最快2步到最后, index: 0 —> 1 -> 4

    	记录在当前能跳到的范围内，看在这个范围内，下一步能跳到最远是哪里 
    	i 的作用是记录上一次能到的最远，所以其实是 i 在遍历，i 的边际不断向 n-1 刷新
    	----------------------------------------------------------------------------------------
    	curMax = 0 									i = 0, res = 1
		preMax = 0		i = 0		curMax = 2		i += 1, res += 1	  跳出循环
		preMax = 2		i = 1		curMax = 4      i += 1
						i = 2 		curMax = 4      i += 1, res += 1    跳出循环
		preMax = 4		i = 3		curMax = 4      i += 1
						i = 4		curMax = 8      i += 1, res += 1    跳出循环并且跳出大循环
    	"""
        n = len(nums)
        curMax, res, i = 0, 0, 0
        while curMax < n - 1:
            preMax = curMax
            while i <= preMax:
                curMax = max(curMax, i + nums[i])
                i += 1
            res += 1
            if preMax == curMax:
                return -1
        return res

        """
		@贪婪算法不是那么好想，毕竟一开始很难想到最远距离
		@动态规划则比较直观, dp[i]记录到达 i 的最小步数, 那么对于

		Input : nums = [2,3,1,1,4,2]
		Expect: dp   = [0,1,1,2,2,3]
        """
        dp = [0] * n
        preMax, pre = nums[0], 0
        curMax = 0
        for i in range(1, n):
        	dp[i] = dp[pre] + 1
        	curMax = max(curMax, i + nums[i])
        	if i == preMax:
        		pre = i
        		preMax = curMax
        return dp[-1]

        		



