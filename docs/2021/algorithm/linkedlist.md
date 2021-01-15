---
title: 链表
date: 2021-01-14
categories:
   - Practice
tags:
   - Leetcode
---

## 1457. Pseudo-Palindromic Paths in a Binary Tree

**问题**：给你一棵二叉树，每个节点的值为 `1 ~ 9`。 找到所有从根到叶子的路径是伪回文的个数

**例子**： 在下面这个图里, `2-1-1`就是一个伪回文(比如 211 可以通过 permutation 变成回文 121)
::: details
1. 由于节点取值范围在 1 ~ 9 考虑用 bit 来表征每一个数，这样path可以表示成类似字符串的 bin()
2. 如何判断一个bin()代表回文呢？ 例如 121 可以表示为 00...010 只有1个中心的1 或者 1221 表示成 00...0 都是0
3. 之前的 path ^ (1 << node.val) 代表包括这一点的 path
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
:::

![1457. Pseudo-Palindromic Paths in a Binary Tree](~@assets/lc-1457.png#center)


## 328. Odd Even Linked List

**问题**：给定一个单链表(比如`1->2->3->4->5->NULL`)，把所有的奇数节点和偶数节点分别排在一起, 返回`1->3->5->2->4->NULL`

- 应当保持奇数节点和偶数节点的相对顺序。

::: details
难点在于判断 while 循环的条件, 要考虑是否存在下一个`odd`节点的问题
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
:::

![328. Odd Even Linked List](~@assets/lc-328.png#center)


## 147. Insertion Sort List

**问题**：对链表(例如`4->2->1->3`)进行插入排序, 返回`1->2->3->4`

- 插入排序每次只移动一个元素
- 跟打牌一样

::: details
难点在于判断 while 循环的条件, 要考虑是否存在下一个`odd`节点的问题
```python

```
:::

![147. Insertion Sort List](~@assets/lc-147.gif#center)