---
title: 图 和 树
date: 2021-01-03
categories:
   - Practice
tags:
   - Leetcode
---

<big>跳跃游戏</big>
::: right
🎙️ 把所有跳跃游戏总结到一起
:::

::::: tabs type: card
:::: tab 55. I
## 55. Jump Game I
**问题**: 每个元素的值代表你能跳的最大长度, 例如`input=[2,3,1,1,4]`, ==问你能不能从第一个跳到最后一个位置==
::: details
贪婪算法： 统计当前能够走到的最远的地方, 如果最远的地方到不了`current index`, 说明到不了当前这个位置, 自然也就到不了最后一个位置
```python
def canJump(self, nums: List[int]) -> bool:
    reach = 0; n = len(nums)
    for i, num in enumerate(nums):
        if reach < i:
            return False
        reach = max(reach, i+num)
        if reach >= n - 1:
            return True
    return True
```
:::
![45. Jump Game II](~@assets/lc-45.png#center)
::::
:::: tab 45. II
## 45. Jump Game II
**问题**: 每个元素的值代表你能跳的最大长度, 例如`input=[2,3,1,1,4]`, ==问你最短几步可以从第一个跳到最后一个==
::: details 贪心法
在确定当前这一步的时候, 看未来哪一步能跳的最远, 
1. 使用一个`cur`代表当前能到达的最远位置
2. 使用`pre`表示上一次能到达的最远位置
3. 从还没检查过的节点开始, 一直到`pre`, 更新当前能达到的最远距离, 更新`cur`
4. 如果当前位置`cur >= n-1`代表能够到达最后一个位置了
```python
def jump(self, nums: List[int]) -> int:
    pre, cur = 0, 0
    N, step = len(nums), 0; i = 0
    while cur < N - 1:
        pre = cur
        while i <= pre:
            cur = max(cur, nums[i] + i)
            i += 1
        step += 1
    return step
```
:::
::: details BFS法
用一个`queue`去存上面那个`while loop`里的数, 跟前面那个做法基本一模一样, 注意`pre`和`cur`的范围
```python
def jump(self, nums: List[int]) -> int:
    q = collections.deque([0])
    pre, cur, N, step = 0, 0, len(nums), 0
    while q:
        for _ in range(len(q)):
            i = q.popleft()
            if i >= N-1: return step
            cur = max(cur, nums[i] + i)
            for i in range(pre+1, cur+1):
                q.append(i)
            pre = cur
        step += 1
    return step
```
:::
![45. Jump Game II](~@assets/lc-45.png#center)
::::
:::: tab 1306. III
## 1306. Jump Game III
**问题**: ==这次只能跳到`i-arr[i]`或者`i+arr[i]`两个位置==, 给定 `input=[2,0,3,1,1,4]` 和起始位置 `input=5`, ==问你从下标为5的地方开始, 能否跳到任意一个元素值为0的地方==
::: details
```python

```
:::
::::
:::: tab 1345. IV
## 1345. Jump Game IV
**问题**: ==这一次你只能跳到元素值相同的其他地方去==, 要么就只能**移动一格**到别的数字上去, 给定 `arr = [100,-23,-23,404,100,23,23,23,3,404]`, 问你从开头跳到结尾最短几步
::: details
和上面那道题类似, 就是把这一步能到的全部存起来, 但这样会因为一个连续为7的超时, 这个时候其实只用保存头一个和最后一个7即可, 因为其他的只是添加一样的东西到`set`里
```python
def minJumps(self, arr: List[int]) -> int:
    same = collections.defaultdict(list)
    for i, a in enumerate(arr):
        if len(same[a]) > 1 and same[a][-1] + 1 == i:
            same[a].pop()
        same[a].append(i)
    q = collections.deque([0]); visited = [False] * N
    step, N = 0, len(arr)
    while q:
        for i in range(len(q)):
            cur = q.popleft(); visited[cur] = True
            if cur >= N-1: return step
            lst = same[arr[cur]]; lst.append(cur-1); lst.append(cur+1)
            for ncur in lst:
                if 0 <= ncur < N and not visited[ncur]:
                    q.append(ncur)
        step += 1
    return step
```
:::
![1345. Jump Game](~@assets/lc-1345.png#center)
::::
:::: tab 1340. V
## 1340. Jump Game V
**问题**: 题目描述整个变了, 这次你可以选择从数组任意位置开始, 但每次移动只能往数值变小的方向, 问你最多可以访问多少个不同的元素(且每次最多只能跳$d$个单位)

```
arr = [6,4,14,6,8,13,9,7,10,6,12], d = 2
```
::: details
这道题用动态规划作, 根据题意，只能往低了跳，且中间不能遇到比我高的
- `dp[i]`代表从`i`开始跳, 最多可以跳过的台阶数
- 状态转移`dp[i] = max(dp[i], 1+dp[j])`, 一旦有邻近阶梯比`i`高, 停止更新
- 这里特别需要注意的是：要保证DP是从小到大更新(==按顺序更新==), 不然像`[7,6,5,4,3,2,1]`这样的, 不应该从左往右更新
```python
def maxJumps(self, arr: List[int], d: int) -> int:
    N = len(arr); dp = [1] * N
    sorted_arr = [(arr[i], i) for i in range(N)]; sorted_arr.sort()
    for _, i in sorted_arr:
        j = i + 1
        while j < N and j <= i+d and arr[j] < arr[i]:
            dp[i] = max(dp[i], 1 + dp[j]); j += 1
        j = i - 1
        while j >= 0 and j >= i-d and arr[j] < arr[i]:
            dp[i] = max(dp[i], 1 + dp[j]); j -= 1
    print(dp)
    return max(dp)
```
:::
![1340. Jump Game V](~@assets/lc-1340.png#center)
::::
:::::

## 987. Vertical Order Traversal of a Binary Tree

::::: tip 逐列扫描二叉树
**问题**: 一个二叉树, 从左到右竖着看, 每列的结果放到一起, 那么结果是什么样的

**例子**: 比如下面那个图, 答案是`[[4],[2],[1,5,6],[3],[7]]`即从左到右, 从上到下下, 同一层的话则数值从小到大(比如这里的5和6)

:::: tabs type: card
其实重点在于如何得到((-2,2,4),(-1,1,2),(0,0,1),(0,2,5),(0,2,6),(1,1,3),(2,2,7)), 所以我们可以通过DFS或者BFS获得这个这一信息
::: tab DFS
```python
def verticalTraversal(self, root: TreeNode) -> List[List[int]]:

    def dfs(root, x, y):
        if root: 
            m_.append((x,y,root.val))
            dfs(root.left, x-1, y+1)
            dfs(root.right, x+1, y+1)

    m_ = []
    dfs(root, 0, 0)
    res = []; m_.sort()
    pre = float('-inf')
    for x,y,val in m_:
        if x != pre:
            res.append([val]); pre=x
        else:
            res[-1].append(val)
    return res
```
:::
::: tab BFS
```python
def verticalTraversal(self, root: TreeNode) -> List[List[int]]:

    def bfs(root):
        q = collections.deque([(root,0,0)])
        while q:
            cur, x, y = q.popleft()
            m_.append((x,y,cur.val))
            if cur.left:
                q.append((cur.left, x-1, y+1))
            if cur.right:
                q.append((cur.right, x+1, y+1))

    m_ = []
    bfs(root)
    res = []; m_.sort()
    pre = float('-inf')
    for x,y,val in m_:
        if x != pre:
            res.append([val]); pre=x
        else:
            res[-1].append(val)
    return res
```
:::
::::
![987. Vertical Order Traversal of a Binary Tree](~@assets/lc-987.png#center)
:::::

---

## 623. Add One Row to Tre

::::: tip 在树中间插入一行
**问题**: 新添一层值为$v$的节点到二叉树的第$d$层. 见图

**例子**: tree = '[4,2,6,3,1,5]', v = 1, d = 3 (即在第二层所有节点添加$v=1$的子节点)

:::: tabs type: card
::: tab 深度优先
```python
def addOneRow(self, root: TreeNode, v: int, d: int) -> TreeNode:
    if not root: return None
    if d == 1:
        new  = TreeNode(v); new.left = root
        root = new 
    elif d == 2:
        left, root.left   = root.left, TreeNode(v)
        right, root.right = root.right, TreeNode(v)
        root.left.left = left; root.right.right = right
    else:
        self.addOneRow(root.left, v, d-1)    
        self.addOneRow(root.right, v, d-1)    
    return root
```
:::
::: tab 广度优先
```python
def addOneRow(self, root: TreeNode, v: int, d: int) -> TreeNode:
    if d == 1:
        new = TreeNode(v); new.left = root
        return new
    q = collections.deque([root])
    while d > 2:
        for _ in range(len(q)):
            cur = q.popleft()
            if cur.left:  q.append(cur.left)
            if cur.right: q.append(cur.right)
        d -= 1
    while q: # d == 2
        cur = q.popleft()
        tmp = cur.left; cur.left = TreeNode(v); cur.left.left = tmp
        tmp = cur.right; cur.right = TreeNode(v); cur.right.right = tmp
    return root
```
:::
::::

![](~@assets/lc-623.png#center)
:::::

---

## 971. Flip Binary Tree To Match Preorder Traversal

::: tip 找出二叉树的翻转点
__问题__： 如下图所示, 我们希望找到那些需要翻转的点, 让两棵树一模一样, 如果中途发现两棵树怎么转也不可能一样, 返回"[-1]"

```python
"""
必须用一个全局计数器 i 来记录访问voyage的下标
    因为voyage是按照pre-order走的, 你并不知道右子节点的具体下标在哪里
    所以我们其实就是在root上写了一个pre-order遍历, 只是要考虑旋转的问题
"""
def flipMatchVoyage(self, root: TreeNode, voyage: List[int]) -> List[int]:
    
    def dfs(node):
        i = self.i
        if node and i < n:
            if node.val != voyage[i]: 
                self.res = [-1]; return
            self.i += 1
            if node.left and node.left.val != voyage[i+1]:
                self.res.append(node.val)
                dfs(node.right)
                dfs(node.left)
            else:
                dfs(node.left)
                dfs(node.right)
            
    n = len(voyage)
    self.res = []; self.i = 0
    dfs(root)
    if self.res and self.res[0] == -1:
        self.res = [-1]
    return self.res
```
![](~@assets/lc-971.png#center)
:::

---

<big>二叉树排序问题</big>
::: right
🎙️ 记住二叉树每个节点都提供了一个上界/下界
:::

::::: tabs type: card
:::: tab 是否二叉树
## 98. Validate Binary Search Tree
**问题**：判断一棵树是不是BST

::: details
要求 左子树最大值 < cur.val < 右子树最小值, 我们也可以用中序遍历看是否严格升序来判断, ==因为二叉树的中序遍历一定是有序的==
```python                            
def isValidBST(self, root: TreeNode) -> bool:
    
    def helper(root, min_, max_):
        if not root: return True
        if root.val <= min_ or root.val >= max_:
            return False
        return helper(root.left, min_, root.val) and helper(root.right, root.val, max_)
    
    return helper(root, float('-inf'), float('inf'))
```
:::
![98. Validate Binary Search Tree](~@assets/lc-98.png#center)
::::
:::: tab 截取二叉树
## 698. Trim a Binary Search Tree
给定一个二叉搜索树，同时给定 `[L,R]`, 要求保留二叉树中节点值在`[L,R]`的

::: details
如果`node.val > R`, 返回`f(node.left)`, 如果`node.val < L`, 返回`f(node.right)`, 否则保留这个节点, 然后子节点继续
```python
def trimBST(self, root: TreeNode, low: int, high: int) -> TreeNode:
    if not root: return None
    if root.val < low:    return self.trimBST(root.right, low, high)
    elif root.val > high: return self.trimBST(root.left, low,high) 
    else:
        root.left  = self.trimBST(root.left, low, high)
        root.right = self.trimBST(root.right, low, high)
        return root
```
:::
![698. Trim a Binary Search Tree](~@assets/lc-698.png#center)
::::
:::: tab 二叉树累加
## 538. Convert BST to Greater Tree
把BST的每个节点的值重新设置为所有比它值大的节点的值的和。

::: details
```python
def convertBST(self, root: TreeNode) -> TreeNode:
    self.sum = 0
    def helper(root):
        if not root: return None
        helper(root.right)
        self.sum += root.val; root.val = self.sum
        helper(root.left)
    helper(root)
    return root
```
:::
![538. Convert BST to Greater Tree](~@assets/lc-538.png#center)
::::
:::::


## 865. Smallest Subtree with all the Deepest Nodes

::: tip 包含最深叶节点的节点
**问题**：一棵二叉树有它的最大深度，找出一个节点，这个节点包含了所有最大深度的叶子。并且这个节点最接近叶子节点 (不如下图中左下角的`2`包含了所有最深叶子)

```python
"""
我一开始想法比较复杂，设计了一个501个元素的数组，来存储每个节点的高度
其实完全不必要这么做。 往上传递左右平衡(left depth == right depth)的节点,  
    如果左边深就上传左边节点, 右边深就上传右边那个结果
"""
class Solution(object):
    def subtreeWithAllDeepest(self, root):
        return self.depth(root)[1]
        
    def depth(self, root):
        if not root: return 0, None
        l, r = self.depth(root.left), self.depth(root.right)
        if l[0] > r[0]:
            return l[0] + 1, l[1]
        elif l[0] < r[0]:
            return r[0] + 1, r[1]
        else:
            return l[0] + 1, root
```

![865. Smallest Subtree with all the Deepest Nodes](~@assets/lc-865.png#center)
:::

<big>回溯法</big>
::: right
🎙️ 假设前面都是符合要求的(`放在tmp里`), 最后几个位置怎么放
:::

::::: warning
:::: tabs type: card
::: tab 分割回文串
## 131. Palindrome Partitioning

**问题**： 给定一个字符串，找出 **所有可能** 回文子字符串。 
**例子**： 比如 `aaaba` 输出 `[["a","a","a","b","a"],["a","a","aba"], ["a","aa","b","a"],["aa","a","b","a"],  ["aa","aba"],["aaa","b","a"]]`

```python
"""
回溯法经典范例
    在确定当前是回文的条件下，遍历后面字母是回文的可能, 只有是回文, 才加到tmp里
"""
class Solution:
    def partition(self, s: str) -> List[List[str]]:

        def backtrack(cur, tmp):
            if cur > n - 1:
                res.append(tmp[:]); return
            for i in range(cur, n):
                if isPalindrome(s[cur:i+1]):
                    tmp.append(s[cur:i+1])
                    backtrack(i+1, tmp)
                    tmp.pop()

        isPalindrome = lambda s: s == s[::-1]
        res, n = [], len(s)
        backtrack(0, [])
        return res
```

![131. Palindrome Partitioning](~@assets/lc-131.png#center)
:::
::: tab 优美的排列
## 526. Beautiful Arrangement

**问题**： 给定一个数`n`, 你从 `1,2...,n`的所有`permutation`中找出一共有多少种优美排列
- 在优美排列中，第`i`个位置的数字必须要么被`i`整除，要么能够整除`i`

**例子**： 比如给定`n=3`输出`3`，分别是 `[3,2,1],[1,2,3],[2,1,3]`

```python
"""
回溯法经典范例
    回溯法其实就是深度搜索，所以不用考虑并行的情况，用一个数组记录节点是否被访问过即可
"""
class Solution:
    def countArrangement(self, n: int) -> int:
        
        def backtrack(pos, cnt):
            if cnt >= n:
                self.res += 1; return
            for i in range(1, n+1):
                if not visited[i] and ((i % pos == 0) or (pos % i == 0)):
                    visited[i] = 1
                    backtrack(pos+1, cnt+1)
                    visited[i] = 0
                    
        visited = [0] * (n+1)
        self.res = 0
        backtrack(1, 0)
        return self.res
```
:::
::: tab 字母大小排列
## 784. Letter Case Permutation
**问题**： 给定一个字符串S，通过将字符串S中的每个字母转变大小写，我们可以获得一个新的字符串。返回所有可能得到的字符串集合。


```python
"""
回溯法
    一开始我里面用到了循环, 这里不需要, 按顺序一个一个加进去就好
    注意大小写转换的问题
"""
def letterCasePermutation(self, S: str) -> List[str]:
    def backtrack(tmp, ind):
        if ind >= n: 
            res.append(tmp[:]); return
        cur = S[ind]
        if cur.isalpha():
            if cur == cur.upper():
                backtrack(tmp+cur.lower(), ind+1)
            else:
                backtrack(tmp+cur.upper(), ind+1)
        backtrack(tmp+cur, ind+1)
    n = len(S); res = []
    backtrack("", 0)
    return res
```

![784. Letter Case Permutation](~@assets/lc-784.png#center)
:::
::::
:::::

## 127. Word Ladder

:::: tip 拼写修正
**问题**： 给定两个单词(比如`beginWord = 'hit', endWord='cog`)和一个字典(比如`wordList = ["hot","dot","dog","lot","log","cog"]`) 问你从`beginWord`到`endWord`最少多少次转换, 每次转换只能变动一个字母，且必须是字典里的单词
**例子**： 比如上面这个例子，答案是5，因为最短转换序列是 `"hit" -> "hot" -> "dot" -> "dog" -> "cog"`, 长度是`5`
::: details
一. 广度搜索（超时了）
```python
def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
    n, m = len(wordList), len(beginWord)
    visited = set([beginWord])
    que = collections.deque([(beginWord, 1)])
    while que:
        word, res = que.popleft()
        if word == endWord:
            return res
        for i in range(m):
            for j in range(26):
                new_word = word[:i] + chr(97+j) + word[i+1:]
                if new_word in wordList and not new_word in visited:
                    visited.add(new_word)
                    que.append((new_word, res+1))
    return 0
```
二. 双向BFS，就是从终点和起点同时开始向中间搜索，什么时候搜索出现重合，两个不断向中间逼近
```python
def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
    
    def bfs(vis1, vis2, q):
        word, res = q.popleft()
        for i in range(nw):
            for new_word in graph[word[:i]+'*'+word[i+1:]]:
                if new_word in vis2:
                    return vis2[new_word] + res
                if not new_word in vis1:
                    q.append((new_word, res + 1))
                    vis1[new_word] = res + 1
        return None

    graph = defaultdict(set)
    q1,q2 = deque([(beginWord, 1)]), deque([(endWord, 1)])
    vis1,vis2 = {beginWord: 1}, {endWord: 1}
    nw = len(beginWord)

    if endWord not in wordList:
        return 0
    for word in wordList:
        for i in range(nw):
            graph[word[:i]+'*'+word[i+1:]].add(word)
    while q1 and q2:
        dis = bfs(vis1, vis2, q1)
        if dis:
            return dis
        dis = bfs(vis2, vis1, q2)
        if dis:
            return dis
```
:::

![127. Word Ladder](~@assets/lc-127.png#center)
::::

## 1649. Create Sorted Array through Instructions

**问题**：给你一个整数数组 `instructions = [2,5,6,3,4,3]`要求按顺序插入, 然后计算每次插入的cost (cost的计算方法是 min(数组中比他小的元素个数, 数组中比他大的元素个数))
**例子**： 比如上面这个例子，答案是4，因为一开始 `nums = []`
```
    插入 2 ，代价为 min(0, 0) = 0 ，现在 nums = [2] 。
    插入 5 ，代价为 min(1, 0) = 0 ，现在 nums = [2,5] 。
    插入 6 ，代价为 min(2, 0) = 0 ，现在 nums = [2,5,6] 。
    插入 3 ，代价为 min(1, 2) = 1 ，现在 nums = [2,3,5,6] 。
    插入 4 ，代价为 min(2, 2) = 2 ，现在 nums = [2,3,4,5,6] 。
    插入 3 ，代价为 min(1, 3) = 1 ，现在 nums = [2,3,3,4,5,6] 。
    总代价为 1+2+1 = 4 。
```
::: details
用一个叫做树状数组的方法做, 这种方法适合求区间和(sum of value, sum of count, etc)，比如上面这个例子, 需要构建两个方法, 一个是更新树状数组, 一个是提取树状数组的presum, `n-query(x)`的意义在于`n`是目前总共插入的个数, `query(x)`得到树状数组`presum(x)`, 比如`5='0b101'=tree[5] + tree[4]`就是减掉末尾第一个不为`0`的`1`。 这样总个数减掉包含自己的之前的个数，就等于比自己大的数的个数
```python
def createSortedArray(self, instructions: List[int]) -> int:
    def update(k):
        while k <= limit:
            tree[k] += 1
            k += (k & -k)
    def query(k):
        ret = 0
        while k:
            ret += tree[k]
            k -= (k & -k)
        return ret

    limit = max(instructions); tree = [0] * (limit + 1)
    res, MOD = 0, 10**9 + 7
    for n, x in enumerate(instructions):
        res += min(query(x-1), n - query(x))
        update(x)
    return res % MOD
```
:::

![1649. Create Sorted Array through Instructions](~@assets/lc-1649.png#center)


<big>二分法</big>
::: right
🎙️ 这就是个染色问题
:::

::::: warning 
:::: tabs type: card
::: tab 二分图
## 785. Is Graph Bipartite?

__问题__： 设$G=(V,E)$是一个无向图, 是否可以把$V$分成两拨, 使得图中的每一边两端的节点分别属于不同的一拨, 

__例子__： `graph = [[1,3],[0,2],[1,3],[0,2]]`, 分别代表四个顶点所连的节点, 比如$0$连接了$1$, 也连接了$3$, 所以`graph[0] = [1,3]`能得到节点$0$所连的另一端

```python{5,22}
"""
用两种不同的颜色对不同顶点进行染色，相邻顶点染成相反的颜色
    要注意不要重复访问某个节点, 因为这里只有两种颜色，
    所以不存在需要撤销操作的需要(不需要考虑是否有更好的涂色), 颜色加深的两行是精髓
"""
def isBipartite(self, graph: List[List[int]]) -> bool:
    n = len(graph)
    color = [0] * n; q = collections.deque()
    for i in range(n):   #可能节点不是都连在一起的, 所以要遍历所有节点
        if color[i] != 0: continue
        q.append(i); color[i] = 1
        while q:
            cur = q.popleft()
            for ncur in graph[cur]:
                if color[ncur] == color[cur]: return False
                if color[ncur] == 0:
                    q.append(ncur); color[ncur] = -color[cur]
    return True

"""上面是BFS作法, 如果用DFS的话"""
def isBipartite(self, graph: List[List[int]]) -> bool:
    def dfs(node, color):
        if visited[node] != 0: 
            return visited[node] == color
        visited[node] = color
        for nnode in graph[node]:
            if not dfs(nnode, -color): return False
        return True
    n = len(graph); visited = [0] * n
    for i in range(n):
        if visited[i] == 0 and not dfs(i, 1):
            return False
    return True
```

![785. Is Graph Bipartite](~@assets/lc-785.png#center)
:::
::: tab 是否二分
## 886. Possible Bipartition

__问题__： 要把喜欢彼此的人放到一组, 总共两个组

__例子__： `N = 4, dislikes = [[1,2],[1,3],[2,4]]`, 代表有$4$个人, 其中$1$不喜欢$2,3$, $2$不喜欢$4$

```python
"""
和前面那道题差不多, 只是这里我们要用`dislikes`来构建图(节点-节点),
    然后就是同一条线的两端不能染同一个颜色
"""
def possibleBipartition(self, N: int, dislikes: List[List[int]]) -> bool:
    m_ = collections.defaultdict(set)
    color = [0] * (N+1); q = collections.deque()
    for a, b in dislikes:
        m_[a].add(b); m_[b].add(a)
    for i in range(N):
        if color[i] == 0:              color[i] = 1; q.append(i)
        while q:
            cur = q.popleft()
            for ncur in m_[cur]:
                if color[ncur] == 0:   color[ncur] = -color[cur]; q.append(ncur)
                elif color[ncur] == color[cur]:   return False
    return True
```

![785. Is Graph Bipartite](~@assets/lc-785.png#center)
:::
::::
:::::