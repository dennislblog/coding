class Solution:
    """
    @问题： 一个list能否拆成两个sublist, 和相等
    @例子： 比如 nums = [1,5,11,5] 中存在 subset sum[1,5,5] = subset[11]

    @思路： 我一开始的思路是 backtracking 但超时了，原因应该是没有存储中间步骤，这个时间复杂度也是O(n)
    """
    def canPartition(self, nums: List[int]) -> bool:
        total, size = 0, 0
        for num in nums:
            total += num
            size  += 1
        if total % 2: return False
        target, self.res = total >> 1, False
        
        def backtrack(start, sum_):
            if sum_ == target:
                return True
            if sum_ > target:
                return False   
            for i in range(start+1, size):
                if backtrack(i, sum_ + nums[i]):
                    return True
            return False
        
        return backtrack(-1, 0)

    """
    @思路： 这道题用动态规划作，令dp[i][j] = 前 i 个数加起来的和等于 j
                那么我们有  dp[i][j] = dp[i-1][j] or dp[i-1][j - num[i]] 两种情况
                    这个DP可以被压缩，因为 只用到了 i 和 i-1 临近的两步
    @注意： DP压缩以后 j 需要从 target -> num  用一个例子比较明白为什么这么做
    @例子： nums = [1,5,11,5]
    ------------------------
    1）假设从小往大更新 dp[target] = dp[target] or dp[target - num]
    j = (num:=1) -> (target:=11) 
        dp[1] = dp[1] or dp[0] = True
        dp[2] = dp[2] or dp[1] = True  显然不对，只看第一个数字，显然和不可能等于2
    ------------------
    2）假设从大到小更新 dp[target] = dp[target] or dp[target - num]
    j = (target:=11) -> (num:=1)
        dp[11] = dp[11] or dp[10] = False
        ...
        dp[2] = dp[2] or dp[1] = False
        dp[1] = dp[1] or dp[0] = True  这样就对了num只允许被使用一次
    j = (target:=11) -> (num:=5)
        dp[6] = dp[6] or dp[1] = True
        dp[5] = dp[5] or dp[0] = True
    j = (target:=11) -> (num:=11)
        dp[11] = dp[11] or dp[0] = True
    j = (target:=11) -> (num:=5)
        dp[11] = dp[11] or dp[6] = True
        dp[10] = dp[10] or dp[5] = True
        dp[6] = dp[6] or dp[1] = True
        dp[5] = dp[5] or dp[0] = True
    ------------------
    这样收集了所有 subset 和的可能性分别是  1 5 6 10 11
    """
    class Solution:
        def canPartition(self, nums: List[int]) -> bool:
            n, total = len(nums), sum(nums)
            target, cond = divmod(total, 2)
            if cond:
                return False
            dp = [False] * (target + 1); dp[0] = True
            for num in nums:
                for j in range(target, num-1, -1):
                    dp[j] = dp[j] | dp[j - num]
            return dp[target]
            
            