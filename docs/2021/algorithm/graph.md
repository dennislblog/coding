---
title: 图 和 树
date: 2021-01-03
categories:
   - Practice
tags:
   - Leetcode
---

## 1345. Jump Game IV
> Input: arr = [100,-23,-23,404,100,23,23,23,3,404]

> Output: 3 最短跳三下从起点到终点

每一步，你可以从下标 i 跳到下标：
1. i + 1 满足：i + 1 < arr.length
2. i - 1 满足：i - 1 >= 0
3. j 满足：arr[i] == arr[j] 且 i != j

**问题**：返回到达数组最后一个元素的下标处所需的 最少操作次数 。
::: details
因为可以跳跃(相同数字)，因此第一时间想到用图 + 广度搜索来做
```python                            
# 右边相对于左边优化了两点： 1）访问过的节点从 m_ 中释放内存(因为不可能再访问)； 2） 对于每一个数字，不保存连续出现的index(除非首尾)
                                                                                                                                
class Solution:                                            |   class Solution:
    def minJumps(self, arr: List[int]) -> int:             |       def minJumps(self, arr: List[int]) -> int:
        m_, n = collections.defaultdict(set), len(arr)     |           m_, n = collections.defaultdict(list), len(arr)
        res = 0                                            |           res = 0 
        for i, a in enumerate(arr):                        |           for i, a in enumerate(arr):
            m_[a].add(i)                                   |               if len(m_[a]) > 1 and m_[a][-1] + 1 == i:
        q = collections.deque([0]); visited = [0]*n        |                   m_[a].pop()
        while q:                                           |               m_[a].append(i)
            size = len(q)                                  |           q = collections.deque([0]); visited = [0] * n
            for _ in range(size):                          |           while q:
                cur = q.popleft()                          |               size = len(q)
                if cur == n - 1: return res                |               for _ in range(size):
                                                           |                   cur = q.popleft()
                set_ = m_[arr[cur]]                        |                   if cur == n - 1: return res
                if cur + 1 < n: set_.add(cur+1)            |                   lst = m_[arr[cur]]
                if cur - 1>= 0: set_.add(cur-1)            |                   if cur + 1 < n: lst.append(cur+1)
                for ncur in set_:                          |                   if cur - 1>= 0: lst.append(cur-1)
                    if not visited[ncur]:                  |                   for ncur in lst:
                        visited[ncur] = 1                  |                       if not visited[ncur]:
                        q.append(ncur)                     |                           visited[ncur] = 1
            res += 1                                       |                           q.append(ncur)
        return -1                                          |                   m_[cur] = []

                                                           |               res += 1
```
:::

![1345. Jump Game](~@assets/lc-1345.png#center)

## 98. Validate Binary Search Tree 
**问题**：判断一棵树是不是BST
::: details
1. `递归`，要求 左子树最大值 < cur.val < 右子树最小值
```python                            
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        
        def helper(root, min_, max_):
            if not root: return True
            if root.val <= min_ or root.val >= max_:
                return False
            return helper(root.left, min_, root.val) and helper(root.right, root.val, max_)
        
        return helper(root, float('-inf'), float('inf'))
```
2. 也可以直接`in-order`遍历, 如果不是一直升序, 返回False
```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        self.prev = float('-inf')
        def inorder(root):
            if not root:                 return True
            if not inorder(root.left):   return False
            if self.prev >= root.val:     return False
            self.prev = root.val
            if not inorder(root.right):  return False
            return True
        return inorder(root)
```
:::

![98. Validate Binary Search Tree](~@assets/lc-98.png#center)

## 173. Binary Search Tree Iterator
**问题**：写一个中序遍历的迭代器, 要求存储空间不得超过 log(n) 平摊访问时间不超过 O(1)
::: details
最简单的方法是一次性按`inorder`逆向压入所有节点, 但这样存储空间是O(n)，不符合要求。 均摊的思想就是每pop一个左子节点，把这个节点右子树的所有左边节点压入栈中
```python                            
class BSTIterator:

    def __init__(self, root: TreeNode):
        self.stack = [] #max size = height of the tree
        self.addleft(root)

    def addleft(self, root: TreeNode):
        while root:
            self.stack.append(root)
            root = root.left
        
    def next(self) -> int:
        out = self.stack.pop()
        self.addleft(out.right)
        return out.val

    def hasNext(self) -> bool:
        return bool(self.stack)
```
:::

![173. Binary Search Tree Iterator](~@assets/lc-173.png#center)


## 865. Smallest Subtree with all the Deepest Nodes

**问题**：一棵二叉树有它的最大深度，找出一个节点，这个节点包含了所有最大深度的叶子。并且这个节点最接近叶子节点 (不如下图中左下角的`2`包含了所有最深叶子)
::: details
我一开始想法比较复杂，设计了一个501个元素的数组，来存储每个节点的高度, 其实完全不必要这么做。 往上传递左右平衡(`left depth == right depth`)的节点, 如果左边深就上传左边节点, 右边深就上传右边那个结果
```python
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
:::


![865. Smallest Subtree with all the Deepest Nodes](~@assets/lc-865.png#center)


## 131. Palindrome Partitioning

**问题**： 给定一个字符串，找出 **所有可能** 回文子字符串。 
**例子**： 比如 `aaaba` 输出 `[["a","a","a","b","a"],["a","a","aba"], ["a","aa","b","a"],["aa","a","b","a"],  ["aa","aba"],["aaa","b","a"]]`
::: details
回溯法经典范例, 在确定当前是回文的条件下，遍历后面字母是回文的可能, `只有是回文, 才加到tmp里`
```python
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
:::

![131. Palindrome Partitioning](~@assets/lc-131.png#center)

## 526. Beautiful Arrangement

**问题**： 给定一个数`n`, 你从 `1,2...,n`的所有`permutation`中找出一共有多少种优美排列
- 在优美排列中，第`i`个位置的数字必须要么被`i`整除，要么能够整除`i`

**例子**： 比如给定`n=3`输出`3`，分别是 `[3,2,1],[1,2,3],[2,1,3]`
::: details
回溯法经典范例, 回溯法其实就是深度搜索，所以不用考虑并行的情况，用一个数组记录节点是否被访问过即可
```python
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

## 127. Word Ladder

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