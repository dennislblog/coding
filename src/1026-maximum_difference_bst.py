class Solution:
    """
    @ 问题:                          8
                            3                10
                        1       6      None        14
                              4   7              13
                        Q: 从这个树里面找差的绝对值最大的
    
    @ solution: 用 BFS 或者 DFS 从上面往下面扫，记录每个节点的 下边界 和 上边界
    @ 改进：好像没有用到 BST 的性质？
    ----------------------------------------------------------------------
    """
    def maxAncestorDiff(self, root: TreeNode) -> int:
        self.res = 0
        
        def dfs(root, _min, _max):
            if not root: return
            _min = min(root.val, _min)
            _max = max(root.val, _max)
            self.res = max(self.res, abs(root.val - _min), abs(root.val - _max))
            dfs(root.left, _min, _max)
            dfs(root.right, _min, _max)
        
        dfs(root, root.val, root.val)
        return self.res