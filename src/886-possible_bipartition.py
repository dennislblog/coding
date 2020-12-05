class Solution:
    """
    @问题： 给定 N = 4, dislikes = [[1,2],[1,3],[2,4]], 代表谁和谁不能分在一组, 问是否可以把N个人分成两组
    @思路： 典型染色问题，用 1 和 -1 两个颜色去标记, 看是否撞色即可
    """
    def possibleBipartition(self, N: int, dislikes: List[List[int]]) -> bool:
        colored = [0] * (N+1)
        neighbors = collections.defaultdict(list)
        for a,b in dislikes:
            neighbors[a].append(b)
            neighbors[b].append(a)
            
        def dfs(i, color):
            colored[i] = color
            for ni in neighbors[i]:
                if colored[ni] == colored[i]:
                    return False
                if not colored[ni] and not dfs(ni, -color):
                    return False
            return True
        
        for i in range(1, N+1):
            if not colored[i] and not dfs(i, 1):
                return False
        return True

    def possibleBipartition(self, N: int, dislikes: List[List[int]]) -> bool:
        # 也可以用iteration去实现DFS
        colored = [0] * (N+1)
        neighbors = collections.defaultdict(list)
        for a,b in dislikes:
            neighbors[a].append(b)
            neighbors[b].append(a)
        
        for i in range(1, N+1):
            if colored[i]: continue
            q = collections.deque([i])
            colored[i] = 1
            while q:
                cur = q.popleft()
                for ncur in neighbors[cur]:
                    if not colored[ncur]:
                        colored[ncur] = -colored[cur]
                        q.append(ncur)
                    elif colored[ncur] == colored[cur]:
                        return False
        return True


"""
@其实所有graph的题都有固定的模板, 比如&207和&210 course schedule problem
"""

class Solution:
    """
    @问题： &207, 给定 numCourses = 2, prerequisites = [[1,0]] 问是否合理, [1,0] 代表上0之前必须先上1
    @思路： 和上面的思路几乎一模一样, 就是要注意`visted设定两个状态, 一个是是否之前遍历过, 另一个是是否正在遍历

    @BFS： 这种题目还有另一种讨巧的做法, 就是剥洋葱, 从入度为0的开始剥, 每剥开一层, 入度减1, 
            最后如果发现有点节点还有入度, 代表剥不干净, 有环
    """
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        visited = [0] * numCourses
        pre = collections.defaultdict(set)
        for a,b in prerequisites:
            pre[b].add(a)
        
        def dfs(x):
            visited[x] = 2
            for prex in pre[x]:
                if visited[prex] == 2:
                    return False
                if not visited[prex] and not dfs(prex):
                    return False
            visited[x] = 1
            return True

        for i in range(numCourses):
            if not visited[i] and not dfs(i):
                return False
        return True

    """
    @问题： &210, 给定 numCourses = 2, prerequisites = [[1,0]] 输出任意一种可以work的plan(上课先后次序)
    @思路： 几乎就是一模一样的思路, 判断有环, 每call一次dfs(x)把x插入到list里
    @相似的题目还有 310. Minimum Height Trees
    """
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        indegree = [0] * numCourses
        pregraph = collections.defaultdict(set)
        res = []
    
        for u,v in prerequisites:
            pregraph[v].add(u)
            indegree[u] += 1
        
        q = deque([])
        for i in range(numCourses):
            if indegree[i] == 0:
                q.append(i)
        while q:
            n = len(q)  #这个似乎不需要, 直接一路到黑就好
            for _ in range(n):
                cur = q.popleft()
                res.append(cur)
                for ncur in pregraph[cur]:
                    indegree[ncur] -= 1
                    if indegree[ncur] == 0:
                        q.append(ncur)
                        
        for i in range(numCourses):
            if indegree[i] != 0:
                return []
        return res
            
