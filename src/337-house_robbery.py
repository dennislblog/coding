# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    """
         3
        / \
       2   5
      / \   \ 
     1   3   1
    @问题： 在binary tree中，找到不相邻节点的最大和，比如上面的最大和是 (1+3 + 5 = 9)
    @思路： 每一个节点需要记住两个值：不包含自己 和 包含自己 的最大值
            - 包含自己的 res[1] = left[0] + right[0] + val
            - 不包含自己 res[0] = max(left) + max(right)
    """
    # 第一次尝试错了（没读懂题）：因为不是逐层比较，右边的5 可以 和 左边的 (1,3) 匹配
    def rob(self, root: TreeNode) -> int:
        # current level and last level
        if not root: return 0
        dp = [0, 0]
        que = deque([root])
        while que:
            cursum = 0
            for _ in range(len(que)):
                cur = que.popleft()
                cursum += cur.val
                if cur.left: que.append(cur.left)
                if cur.right: que.append(cur.right)
            dp[0], dp[1] = dp[1], max(dp[0] + cursum, dp[1])
        return dp[1]
            
    # 好像自上而下做很难，自下而上很好理解
    def rob(self, root: TreeNode) -> int:
        
        def dfs(root):
            # :ret  max sum
            if not root:
                return (0, 0)
            res = [0, 0]
            left = dfs(root.left)
            right= dfs(root.right)
            # exclude cur node: so both left and right can be included
            res[0] = max(left) + max(right)
            # include cur node: so neither left nor right can be included
            res[1] = left[0] + right[0] + root.val
            return res
        
        return max(dfs(root))
        