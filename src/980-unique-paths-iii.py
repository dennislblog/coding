from typing import List


class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        # 1. go over the grid, record where is the start, goal and number of non-obstacle
        # 2. depth first search with backtracking, if we are at the goal make sure record goes to zero, and that is one solution
        # 3. for each square, find its legal neighbor to expand

        n, m = len(grid), len(grid[0])
        self.ans, record = 0, 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 0:
                    record += 1
                elif grid[i][j] == 1:
                    si, sj = i, j
                elif grid[i][j] == 2:
                    ti, tj = i, j

        def neighbor(x, y):
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] == 0 or grid[nx][ny] == 2:
                        yield (nx, ny)

        def dfs(x, y, todo):
            # todo is a local variable tracking the number of non-visisted non-obstacles
            # print("x={},y={},todo={},cur={}".format(x, y, todo, grid[x][y]))
            if x == ti and y == tj:
                if todo == 0:
                    self.ans += 1
                return
            for nx, ny in neighbor(x, y):
                grid[x][y] = -1
                dfs(nx, ny, todo-1)
                grid[x][y] = 0
            return

        dfs(si, sj, record+1)
        return self.ans
