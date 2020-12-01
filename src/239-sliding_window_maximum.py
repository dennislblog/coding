class Solution:
    """
    @问题： 给定一个数列 nums = [1,3,-1,-3,5,3,6,7] 和 一个常数 k 代表窗口大小, 输出每一个window最大值
    @例子：     Window position                Max
                ---------------               -----
                [1  3  -1] -3  5  3  6  7       3
                 1 [3  -1  -3] 5  3  6  7       3
                 1  3 [-1  -3  5] 3  6  7       5
                 1  3  -1 [-3  5  3] 6  7       5
                 1  3  -1  -3 [5  3  6] 7       6
                 1  3  -1  -3  5 [3  6  7]      7
    @思路： 
        1）维护一个priority queue (最大值和对应index) 
        2）当 cur ind - top ind >= k 这样最大值不在当前这个window里，那么pop
    
    @例子: 就上面那个
    ----------------
    cur @1    que=[(0,1)]
    cur @3    que=[(1,3)]
    cur @-1   que=[(1,3),(2,-1  )]                 now 1st max = 3
    cur @-3   que=[(1,3),(2,-1),(3,-3)]            now 2nd max = 3
    cur @5    que=[(4,5)] (with popleft and pop)   now 3rd max = 5
    cur @3    que=[(4,5),(5,3)]                    now 4th max = 5
    ...
    """
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        que = collections.deque() # [[i, num]]
        res = []
        for i, num in enumerate(nums):
            if que and i - que[0][0] >= k:
                que.popleft()
            while que and que[-1][1] <= num:
                que.pop()
            que.append([i, num])
            if i >= k - 1:
                res.append(que[0][1])
        return res