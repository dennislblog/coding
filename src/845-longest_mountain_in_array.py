class Solution:
    """
        @问题：在 [2,1,4,7,3,2,5] 中，找到严格的 A[0] < A[1] < ... A[i] > A[i+1] > ... A[n] 的子序列最大长度
        @思路：在每一个点算到目前为止，左边升序和降序的数目，每次遇到平路或者山谷，就重设counter
        @另一种找波峰的方法不过要借助额外两个数组： 例如上面这个数列 up = [0,1,0,1,0,0,0] down = [1,0,0,3,2,1,0]
        ----------------------------------------------------------------------------------
        example       2     1     4     7     3     2     5 
        up            0     0     1     2     2     2     1
        down          0     1     0     0     1     2     0
        如果 up > 0 and down > 0 代表这个点刚经历了波峰，现在在下坡中；一旦 A[i] = A[i-1] 重新设定
    """
    def longestMountain(self, A: List[int]) -> int:
        res = 0
        n = len(A)
        if n < 3: return res
        up = down = 0
        for i in range(1, n):
            if A[i] == A[i-1] or (down and A[i] > A[i-1]):
                up = down = 0
            if A[i] > A[i-1]:
                up += 1
            if A[i] < A[i-1]:
                down += 1
            if up and down:
                res = max(res, up + down + 1)
        return res