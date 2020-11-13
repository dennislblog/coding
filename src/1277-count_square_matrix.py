class Solution:
    def countSquares(self, matrix: List[List[int]]) -> int:
        """
            @问题：从图里找有多少个 全是1 的矩阵
            @example: 
                    [
                      [0,1,1,1],
                      [1,1,1,1],
                      [0,1,1,1]
                    ]
            @solution: 用动态规划，一行一行的更新，dp[i,j]: 以[i,j]作为右下角的`全是1`矩阵的个数
                       if (i,j) == 1:
                            dp[i,j] = min(dp[i-1,j], dp[i,j-1], dp[i-1,j-1]) +  1   #这个是关键
                       else:
                            dp[i,j] = 0
            @注意:  - 如果不想用二维矩阵，需要特别注意，我并没有dp[i-1,j-1]的信息，因此需要创建一个临时向量
                    这样不至于丢失上一行的DP信息，用临时向量tmp to track dp[i][j-1]
                    - 另外一个需要注意的就是非primitive的复制，需要用到copy()否则复制的只是指针
            -------------------------------------------------------------------------------
            :iter row               :dp
            1 (indx=0)              [0, 1, 1, 1]
            2                       [1, 1, 2, 2]
            3                       [0, 1, 2, 3]       
        """
        nr, nc = len(matrix), len(matrix[0])
        dp = matrix[0].copy(); res = sum(dp)
        for i in range(1, nr):
            tmp = [matrix[i][0]]
            for j in range(1, nc):
                if matrix[i][j]==1: 
                    tmp.append(min(dp[j-1], tmp[-1], dp[j]) + 1)
                else:
                    tmp.append(0)
            dp = tmp[:]    
            res += sum(dp)
            print(dp)
        return res