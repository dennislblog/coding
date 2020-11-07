class Solution(object):
    """
    @ 问题： in binary search tree, exactly two nodes of the tree were swapped by mistake
            @ example: [1,3,null,null,2] ==> 1和3需要调换
            --------------------------------------------
            inorder traversal 
            swap
    """
    def recoverTree(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """
        # 1. 按顺序遍历二叉树；2. 4-2-1-3 先找到不符合的`4`, 然后找到最后一个不符合的`1` 3. 因为只有这两个不符合条件
        self.pre, self.first, self.second = None, None, None
        
        def inorder(root):
            if not root: return None
            inorder(root.left)
            if self.pre and self.pre.val > root.val:
                if not self.first:
                    self.first = self.pre
                self.second = root
            self.pre = root
            inorder(root.right)
        
        
        inorder(root)
        self.first.val, self.second.val = self.second.val, self.first.val