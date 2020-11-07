class Solution:
    """
    @ 问题：Two nodes of a binary tree are cousins if they have the same depth, but have different parents.

        @ example:  [1,2,3,4] x=4, y=3 ==> return False 因为 4 和 3 不在同一层
        ---------------------------------------------------------------------
    """
    def isCousins(self, root: TreeNode, x: int, y: int) -> bool:
        # 1. 使用BFS遍历树的每一层，将下一层所有结点放到一个set中 (注意x,y 同 parent 情况)
        # 2. 在这一层中判断 x, y 是否出现在 set 里
        if root.val == x or root.val == y:
            return False
        q = {root}
        while q:
            tmp = set()
            for node in q:
                if node.left and node.right:
                    if set([node.left.val, node.right.val]) == set([x, y]):
                        return False
                    tmp.add(node.left)
                    tmp.add(node.right)
                else:
                    tmp.add(node.left or node.right)
            q = {n for n in tmp if n is not None}
            values = {n.val for n in q}
            if x in values and y in values:
                return True
            if x in values or y in values:
                return False
        return False