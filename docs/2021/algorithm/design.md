---
title: 设计题
date: 2021-02-08
categories:
   - Practice
tags:
   - Leetcode
---


## 284. Peeking Iterator

__问题__： 设计迭代器类的接口，接口包含两个方法： `next()` 和 `hasNext()`. 

::: details
这道题的难点在于如何不调用`next`就能知道`iterator`的下一个元素呢? 答案是提前把这个元素存起来

```python
class PeekingIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self._next = iterator.next()

    def peek(self):
        return self._next
        
    def next(self):
        ret = self._next
        if self.iterator.hasNext():
            self._next = self.iterator.next()
        else:
            self._next = None
        return ret

    def hasNext(self):
        return self._next != None
```
:::

```
假设迭代器被初始化为列表 [1,2,3]。

调用 next() 返回 1，得到列表中的第一个元素。
现在调用 peek() 返回 2，下一个元素。 在此之后调用 next() 仍然返回 2。
最后一次调用 next() 返回 3，末尾元素。 在此之后调用 hasNext() 应该返回 False。
```


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