class Solution:
    """
    @问题：Two nodes of a binary tree are cousins if they have the same depth, but have different parents.

        @example:      1
                    2     3
                 4             this is a binary tree, judge whether x=3 and y=4 are cousins       
        -----------------------------------------------------------------------------------
    @思路： BFS or DFS 
    """

    # 1. DFS: vertical traversal ==> return (parent, height)

    def isCousins(self, root: TreeNode, x: int, y: int) -> bool:
        
        # ox = (parent.val, cur.height)
        ox, oy = [0,0],[0,0]
        
        def dfs(root, parent, height):
            if not root: return 
            if root.val == x:
                ox[0], ox[1] = parent.val, height
            elif root.val == y:
                oy[0], oy[1] = parent.val, height
            dfs(root.left, root, height+1)
            dfs(root.right, root, height+1)
            
        dfs(root, root, 0)

        if ox[0] != oy[0] and ox[1] == oy[1]:
            return True
        else:
            return False

    # 2. BFS: we don't have to count height, just check (x,y) and their parent in the same level

    def isCousins(self, root: TreeNode, x: int, y: int) -> bool:

        px, py = 0, 0
        q, height = deque([(root, 0)]), 0
        
        while q:
            size = len(q)
            for i in range(size):
                cur, parent = q.popleft()
                if cur.val == x:
                    px = parent
                if cur.val == y:
                    py = parent
                if cur.left:
                    q.append((cur.left, cur.val))
                if cur.right:
                    q.append((cur.right, cur.val))
            if (px==0) ^ (py==0): #if px != 0 and py = 0 or vice versa, they are not in the same level
                return False
            if px != py:
                return True
        return False