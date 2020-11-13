class Solution:
    """
        @问题：给定一个数列，找出所有不重复的permutation, e.g., [1,1,1,2] => 
        @solution： backtrack + DFS
            1. 用一个visited数组判断当前partial lst里面是否已经包含nums[i]
            2. 如何过滤重复？ 如果前一个已经被包括，这一个还是可以放进来(因为已经被排序)
            3. 确保 visited数组  和  partial lst 放回去 (backtracking)
        --------------------------------------------------------------------------
                        recursion stack                         visited
        @dfs([1], 1)                                            [1,0,0,0]
            @dfs([1,1], 2)                                     
                @dfs([1,1,1], 3)                               
                    @dfs([1,1,1,2], 4)                          
                @dfs([1,1,2], 3)                                [1,1,0,1]
                    @dfs([1,1,2,1], 4)                          
        # here the 3rd 1 is bypassed because visited[1] = False at this moment !
            @dfs([1,2], 2)                                      [1,0,0,1]
        # here the same thing happend, 3rd 1 is bypassed
                @dfs([1,2,1], 3)                                [1,1,0,1]
                    @dfs([1,2,1,1], 4)                          
        @dfs([2], 1)

    """
    def permuteUnique(self, nums: list) -> list:
        n, res = len(nums), []
        nums.sort()
        visited = [False] * n
        
        def dfs(tmp, ntmp):
            # :param tmp  = partial result
            # :param ntmp = size of partial result
            # because nums is already sorted (critical point)
            if ntmp == n: 
                res.append(tmp.copy())
                return
            for i, num in enumerate(nums):
                if not visited[i]:
                    if i > 0 and num == nums[i-1] and not visited[i-1]:
                        continue
                    visited[i] = True
                    tmp.append(num); dfs(tmp, ntmp+1); tmp.pop()
                    visited[i] = False
            
        dfs([],0)
        return res
                    

    # 可以用iteration吗？