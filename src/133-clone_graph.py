"""
# Definition for a Node.
class Node(object):
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution(object):
    def __init__(self):
        self.visited = dict()
    def cloneGraph(self, node):
        """
        :type node: Node
        :rtype: Node
        """
        # dfs
        # if not node: return None
        # if node in self.visited: return self.visited[node]
        # new = Node(node.val, [])
        # self.visited[node] = new
        # if node.neighbors:
        #     new.neighbors = [self.cloneGraph(x) for x in node.neighbors]
        # return new
        
        # bfs
        if not node: return None
        queue = deque([node])
        copy_node = Node(node.val, [])
        self.visited[node] = copy_node
        while queue:
            cur = queue.popleft()
            for ncur in cur.neighbors:
                if not ncur in self.visited:
                    copy_ncur = Node(ncur.val, [])
                    self.visited[ncur] = copy_ncur
                    queue.append(ncur)
                self.visited[cur].neighbors.append(self.visited[ncur]) 
        return copy_node
            
        
        
        
        