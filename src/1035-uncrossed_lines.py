class Solution:
    """
    @问题： 例如 A = [1,4,2] and B = [1,2,4]

                1   4   2
                |     \
                1   2   4
        最多可以有两条不相交的边

    @思路： 用动态规划, 
        dp[i][j] 代表 A[0:i] 和 B[0:j] 的结果，于是有
            if A[i] = B[j]: dp[i][j] = dp[i-1][j-1] + 1
            else          : dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        由于在动态规划中仅仅用到了相邻两行的信息，即左边,上面和左上角, 因此我们可以只保存最近两行的dp

    @例子: 就上面那个
    ----------------
    a = 1
        b = 1   dp = [0, 1, 0, 0]
        b = 2   dp = [0, 1, 1, 0]
        b = 4   dp = [0, 1, 1, 1]
    a = 4
        b = 1   dp = [0, 1, 0, 0]
        b = 2   dp = [0, 1, 1, 0]
        b = 4   dp = [0, 1, 1, 2]
    a = 2
        b = 1   dp = [0, 1, 0, 0]
        b = 2   dp = [0, 1, 2, 0]
        b = 4   dp = [0, 1, 2, 2]
    """
    def maxUncrossedLines(self, A: List[int], B: List[int]) -> int:
        na, nb = len(A), len(B)
        dp = [0] * (nb + 1)
        for a in A:
            prev = dp[:]
            for i, b in enumerate(B):
                if a == b:
                    dp[i+1] = 1 + prev[i] 
                else:
                    dp[i+1] = max(dp[i], prev[i+1])
        return dp[-1]


        
"""
@类似的利用动态规划解题的还有经典的`Edit Distance问题, 
    解决动态规划问题：
        1) 确定dp的意义
        2) 确定转移方程
        3) 查看edge case, 比如这里要特别注意 dp[0] = i + 1这个点
"""


class Solution:
    """
    @问题： 给定  word1 = "horse", word2 = "ros" 返回多少个操作可以让 word1 -> word2 (删除,增加和替换都是 1 的操作)
    """
    def minDistance(self, word1: str, word2: str) -> int:
        n1, n2 = len(word1), len(word2)
        dp = list(range(n2+1))
        for i, w1 in enumerate(word1):
            pre = dp[:]; pre[0] = i; dp[0] = i+1
            for j, w2 in enumerate(word2):
                if w1 == w2:
                    dp[j+1] = pre[j]
                else:
                    dp[j+1] = min(dp[j],pre[j],pre[j+1])+1
        return dp[-1]