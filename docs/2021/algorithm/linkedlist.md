---
title: 链表
date: 2021-01-14
categories:
   - Practice
tags:
   - Leetcode
---

## 234. Palindrome Linked List

:::: tip
__问题__： 判断一个链表是不是回文链表。

::: warning
![](~@assets/lc-234.png#right)
思路：
1. 最简单, 逐个读取到数组, 然后判断数组=逆数组?
2. 用栈逆序存储前面一半的节点, 和后面一半逐个比较
3. 大神的回答, 直接在遍历的时候创建双向链表(见代码)
:::

```python
"""
    null <-- 1 <--> 2 --> 3 --> 2 --> 1
                   rev         slow  
"""
def isPalindrome(self, head: ListNode) -> bool:
    rev = None
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow, rev, rev.next = slow.next, slow, rev
    if fast: # 如果是奇数个节点,少算了一个
        slow = slow.next
    while rev and rev.val == slow.val:
        rev = rev.next
        slow = slow.next
    return not rev
```
::::

## 1457. Pseudo-Palindromic Paths in a Binary Tree

:::: tip 

**问题**：给你一棵二叉树，每个节点的值为 `1 ~ 9`。 找到所有从根到叶子的路径是伪回文的个数

```bash
输入：root = [2,1,1,1,3,null,null,null,null,null,1]
输出：1 
解释：总共有 3 条从根到叶子的路径：路径 [2,1,1] ，路径 [2,1,3,1] 和路径 [2,1] 
     这些路径中只有红色路径是伪回文路径，因为 [2,1,1] 存在回文排列 [1,2,1] 
```
::: warning 
1. 由于节点取值范围在 1 ~ 9 考虑用 bit 来表征每一个数，这样path可以表示成类似字符串的 bin()
2. 如何判断一个bin()代表回文呢？ 例如 121 可以表示为 00...010 只有1个中心的1 或者 1221 表示成 00...0 都是0
3. 之前的 path ^ (1 << node.val) 代表包括这一点的 path
:::

```python                            
def pseudoPalindromicPaths (self, root: TreeNode) -> int:

    def dfs(root, cnt):
        if not root: return 0
        cnt = cnt ^ (1 << root.val)
        if not root.left and not root.right:
            if cnt == 0 or (cnt & cnt-1) == 0:
                self.res += 1
            return 0
        dfs(root.left, cnt); dfs(root.right, cnt)

    self.res = 0;  dfs(root, 0)
    return self.res
```
![1457. Pseudo-Palindromic Paths in a Binary Tree](~@assets/lc-1457.png#center)

::::

## 328. Odd Even Linked List

:::: tip 
**问题**：给定一个单链表，把所有的奇数节点和偶数节点分别排在一起

```bash
输入: 2->1->3->5->6->4->7->NULL 
输出: 2->3->6->7->1->5->4->NULL
解释：应当保持奇数节点和偶数节点的相对顺序
```

::: warning
![328. Odd Even Linked List](~@assets/lc-328.png#right)
难点在于判断 while 循环的条件
- 要考虑`even.next=odd.next`中`odd`是否为空的问题 
- 用两个指针分别控制奇数和偶数, 最后通过`firstEven`连起来
:::
```python
def oddEvenList(self, head: ListNode) -> ListNode:
    if not head: return head
    odd, even = head, head.next
    firstEven = even
    while even and even.next:
        odd.next = even.next; odd = odd.next
        even.next = odd.next; even = even.next
    odd.next = firstEven
    return head
```

::::

## 147. Insertion Sort List

:::: tip
![147. Insertion Sort List](~@assets/lc-147.gif#right)
**问题**：对链表(例如`4->2->1->3`)进行插入排序, 返回`1->2->3->4`

- 插入排序每次只移动一个元素
- 跟打牌一样
- 难点在于判断 while 循环的条件, 要考虑是否存在下一个`odd`节点的问题

```python

```
::::


## 141. Linked List Cycle
:::: tip 
**问题**： 如果链表中存在环, 则返回 true, 否则, 返回 false 
```bash
输入：head = [3,2,0,-4], pos = 1
输出：True
```

::: warning
![141. Linked List Cycle](~@assets/lc-141.png#right)
快慢指针搞定, 注意两个特殊情况 `[1]`和`[]`
- 循环下去，只要两者能够重逢说明有环
:::

```python
def hasCycle(self, head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow = head; fast = head.next
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next; fast = fast.next.next
    return True
```
::::


## 138. Copy List with Random Pointer 

**问题**：复制一个复杂链表，这个复杂链表是指出了`value`和`next`指针外，还有一个`random`指针可能指向任何位置的链表节点或空

:::: tabs type: card
::: tab HashMap存储
- 第一遍只复制节点的`val`, `random, next`暂时为空，并将源节点和克隆节点形成映射存放在一个字典里
- 第二遍从
```python
def copyRandomList(self, head: 'Node') -> 'Node':
    if not head: return None
    m_ = {None: None}; cur = head
    while cur:
        m_[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        m_[cur].next = m_[cur.next]
        m_[cur].random = m_[cur.random]
        cur = cur.next
    return m_[head]
```
:::
::: tab 不需要额外存储
1. 复制源节点
2. 生成克隆节点的随机指针
3. 将原链表和克隆链表分离
```python
def copyRandomList(self, head: 'Node') -> 'Node':
    # 先生成1->1'->2->2'->4->4'这样子
    p = head
    while p:
        tmp = Node(p.val)
        p.next, tmp.next = tmp, p.next
        p = tmp.next
    # 复制random
    p = head
    while p:
        if p.random:
            p.next.random = p.random.next
        p = p.next.next
    # 分裂成两个链表
    dummy = Node(-1)
    origin = dummy; clone = head
    while clone:
        origin.next = clone.next
        clone.next = clone.next.next
        origin, clone = origin.next, clone.next
    return dummy.next
```
:::
::::

![138. Copy List with Random Pointer ](~@assets/lc-138.png#center)