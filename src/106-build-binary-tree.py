from typing import List

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        # recursively build tree; note that subtrees are well seperated in both inorder and postorder
        posmap, size = dict(), 0
        for i, num in enumerate(inorder):
            posmap[num] = i
            size += 1

        def buildBinary(ini, inj, poi, poj):
            if ini > inj or poi > poj:
                return None
            headnum = postorder[poj]
            head = TreeNode(headnum)
            curpos = posmap[headnum]
            leftlen = curpos - ini
            head.left = buildBinary(ini, curpos-1, poi, poi+leftlen-1)
            head.right = buildBinary(curpos+1, inj, poi+leftlen, poj-1)
            return head

        return buildBinary(0, size-1, 0, size-1)


if __name__ == "__main__":
    inorder = [9, 3, 15, 20, 7]
    postorder = [9, 15, 7, 20, 3]
    head = Solution().buildTree(inorder, postorder)
    print(isinstance(head, TreeNode))
