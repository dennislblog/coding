class Solution:
    """
        @问题： 从BST里找到第 `k` 小的数字
    """
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        # 
        # Recursive Method
        #    1. inorder traversal with generator
        #    2. yield from g:= for v in g: yield v
        #
        def traverse(node):
            if node:
                yield from traverse(node.left)
                yield node
                yield from traverse(node.right)
        
        k -= 1  # i starts from 0
        for i, node in enumerate(traverse(root)):
            if i == k:
                return node.val


    def kthSmallest(self, root: TreeNode, k: int) -> int:
        """
            Iterative Method
                1. keep adding left node
                2. pop `h` out, and return if cnt == k
                3. move to right branch of `h`
        """
        cur = root; stack = []
        while stack or cur: 
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop(); k -= 1
            if k == 0:
                return cur.val
            cur = cur.right
        return -1
