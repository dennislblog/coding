---
title: 矩阵
date: 2021-01-02
categories:
   - Practice
tags:
   - Leetcode
---

## 289. Game of Life (M)
> Input: board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]

> Output: [[0,0,0],[1,0,1],[0,1,1],[0,1,0]] in-place替换

一个矩阵，每一个位置两种状态： 0代表死细胞；1代表活细胞，在下一个生命周期会发生：
1. 如果活细胞周围八个位置的活细胞数少于两个，则该位置活细胞死亡
2. 如果活细胞周围八个位置有两个或三个活细胞，则该位置活细胞仍然存活
3. 如果活细胞周围八个位置有超过三个活细胞，则该位置活细胞死亡
4. 如果死细胞周围正好有三个活细胞，则该位置死细胞复活

**问题**：已知当前周期细胞状态，求下一个周期的状态，要求 in-place 替换
::: details
设定4个状态，这里的难点在于`in-place`替换
		状态0： 死细胞转为死细胞
        状态1： 活细胞转为活细胞
        状态2： 活细胞转为死细胞
        状态3： 死细胞转为活细胞
那么 1 和 2 在当前状态都是活细胞；而 0 和 3 在当前状态都是死细胞 (用对2取余判断)，这样前面的改动就不影响后面的判定了。然后针对每一个位置, 遍历周围的8个细胞，数有多少个活细胞，进行判定
```python                            
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m, n = len(board), len(board[0])
        dif = ((-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1),(1,0),(1,1))
        for x in range(m):
            for y in range(n):
                num_live = 0
                for (dx, dy) in dif:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and 1 <= board[nx][ny] <= 2:
                        num_live += 1
                if board[x][y] == 1 and (num_live < 2 or num_live > 3):
                    board[x][y] = 2
                elif board[x][y] == 0 and num_live == 3:
                    board[x][y] = 3
        for x in range(m):
            for y in range(n):
                board[x][y] %= 2
```
:::

![289. Game of Life](~@assets/lc-289.png#center)


## 59. Spiral Matrix II (M)
> Input: n = 3

> Output: [[1,2,3],[8,9,4],[7,6,5]] (如何所示按顺序打印)

**问题**：第`54. Spiral Matrix`是这道题的逆操作, 即给定矩阵, 输出螺旋路径
::: details
- 记得标记已经访问过的节点，避免重复访问
```python                            
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        dirs = ((0,1),(1,0),(0,-1),(-1,0)); cur = 0
        res, i, j = [], 0, 0
        nr, nc = len(matrix), len(matrix[0])
        for _ in range(nr * nc):
            res.append(matrix[i][j])
            matrix[i][j] = 0
            next_i, next_j = i + dirs[cur][0], j + dirs[cur][1] 
            cond = next_i < 0 or next_i >= nr or next_j < 0 or next_j >= nc or matrix[next_i][next_j] == 0
            if cond:    cur = (cur+1)%4
            i, j = i + dirs[cur][0], j + dirs[cur][1] 
        return res
```
:::

![59. Spiral Matrix II](~@assets/lc-59.png#center)


## 885. Spiral Matrix III
> Input: $R = 5, C = 6, r_0 = 1, c_0 = 4$ (矩阵的长宽和起始点的位置)

> Output: ...

**问题**：所有在矩阵内按螺旋丸经历的点 --- 暴力破解即可, 当访问点在RC范围内, 加到结果中
::: details
暴力破解即可, 当访问点在RC范围内, 加到结果中
```python
def spiralMatrixIII(self, R: int, C: int, r0: int, c0: int):

    def next(x, y):
        yield (x,y)
        step, cur = 1, 0 
        while True:
            for _ in range(2):     
                for _ in range(step):     
                    x, y = x + dirs[cur][0], y + dirs[cur][1]     
                    yield (x,y)    
                cur = (cur + 1) % 4          # change direction
            step += 1      #each stepsize repeats twice (see pic)

    dirs = ((0,1),(1,0),(0,-1),(-1,0))
    res, cnt = [], 0   
    for i, j in next(r0, c0):      
        if 0 <= i < R and 0 <= j < C:       
            res.append([i, j])           
        if cnt == R*C:         
            break
    return res
```
:::

![885. Spiral Matrix III](~@assets/lc-885.png#center)


## 1329. Sort the Matrix Diagonally

**问题**：将同一条对角线上的元素（从左上到右下）按升序排序后，返回排好序的矩阵

::: details
用一个堆存放对角线元素, 然后一个一个pop出来, 也可以用list-sort-pop
> 对角线元素的$(i-j)$是一样的

```python
def diagonalSort(self, mat: List[List[int]]) -> List[List[int]]:
    lsts = collections.defaultdict(list)
    m, n = len(mat), len(mat[0])
    for i in range(m):
        for j in range(n):
            heapq.heappush(lsts[i-j], mat[i][j])
    for i in range(m):
        for j in range(n):
            mat[i][j] = heapq.heappop(lsts[i-j])
    return mat
```
:::

![1329. Sort the Matrix Diagonally](~@assets/lc-1329.png#center)

## 1091. Shortest Path in Binary Matrix 

**问题**：从左上角到右下角, 中间`0`代表可以通过, `1`代表不能通过, ==方向可以允许↖, ↗, ↙, ↘ 这种==

::: details
典型的BFS的题, 当该节点没有被访问且在矩形内, 就可以扩展节点, 还可以用A*配合优先队列做, 但复杂度我觉得是一样的？

```python
def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    if n== 1:
        return 1
    dirs = ((0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1))
    res = 1; q = collections.deque([(0,0)])
    while q:
        for _ in range(len(q)):
            y, x = q.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if nx == n-1 and ny == n-1:
                    return res + 1
                elif 0 <= nx < n and 0 <= ny < n and grid[ny][nx]==0:
                    grid[ny][nx] = -1
                    q.append((ny, nx))
        res += 1
    return -1
```
:::

![1091. Shortest Path in Binary Matrix](~@assets/lc-1091.png#center)



## 1091. Shortest Path in Binary Matrix 

**问题**：上面一条边和左边一条边代表的是太平洋，右边一条边和下边一条边代表的是大西洋。现在告诉你水往低处流，问哪些位置的水能同时流进太平洋和大西洋？

__例子__： 答案是列出矩阵中能同时流入太平洋和大西洋的格子的坐标

```
Pacific ~   ~   ~   ~   ~ 
   ~  1   2   2   3  (5) *
   ~  3   2   3  (4) (4) *
   ~  2   4  (5)  3   1  *
   ~ (6) (7)  1   4   5  *
   ~ (5)  1   1   2   4  *
      *   *   *   *   * Atlantic
```

:::: tabs type: card
思路就是从陆地边缘开始疯狂试探便可
::: tab dfs
```python
def pacificAtlantic(self, matrix: List[List[int]]) -> List[List[int]]:
    if not matrix: return []
    m, n = len(matrix), len(matrix[0])
    pac, alt = set(), set()
    stack = [(i,0) for i in range(m)] + [(0,j) for j in range(1, n)]
    while stack:
        i, j = stack.pop()
        pac.add((i,j))
        for ni, nj in ((i,j-1),(i,j+1),(i-1,j),(i+1,j)):
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] >= matrix[i][j] and not (ni,nj) in pac:
                stack.append((ni,nj))
    stack = [(i,n-1) for i in range(m)] + [(m-1,j) for j in range(n-1)]
    while stack:
        i, j = stack.pop()
        alt.add((i,j))
        for ni, nj in ((i,j-1),(i,j+1),(i-1,j),(i+1,j)):
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] >= matrix[i][j] and not (ni,nj) in alt:
                stack.append((ni,nj))
    return list(pac & alt)
```
:::
::: tab bfs
```python
def pacificAtlantic(self, matrix: List[List[int]]) -> List[List[int]]:
    if not matrix: return []
    
    def bfs(cover):
        q = collections.deque(cover)
        while q:
            i, j = q.popleft()
            cover.add((i,j))
            for ni, nj in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
                if 0<=ni<m and 0<=nj<n and matrix[ni][nj] >= matrix[i][j] and not (ni,nj) in cover:
                    q.append((ni,nj))
        
    m, n = len(matrix), len(matrix[0])
    pac, alt = set(), set()
    for i in range(m):
        pac.add((i,0)); alt.add((i,n-1))
    for j in range(n):
        pac.add((0,j)); alt.add((m-1,j))
    bfs(pac); bfs(alt)
    return list(pac & alt)
```
:::
::::