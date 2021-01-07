---
title: 链表
date: 2021-01-03
categories:
   - Practice
tags:
   - Leetcode
---

## 82/83. Remove Duplicates from Sorted List I/II

**问题**：给定一个链表(如`1->2->3->3->4->4->5`)，删除里面出现重复的数字，即得到`1->2->5`。 `83`题是要求每个元素只出现一次(就是保留重复的元素)

::: details
关键在于怎么检测 `b` 节点没有挪动过, 如果 `b=a.next` 出现了重复, 那么`b' != a.next` 这种情况下只需要把 `a.next` 挪到 `b'+1`的位置即可 
```python                            
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        dummy = ListNode(-1000); dummy.next = head
        a, b = dummy, dummy.next
        while b and b.next:
            while b and b.next and b.val == b.next.val:
                b = b.next
            if id(a.next) == id(b):
                a = a.next
            else:
                a.next = b.next
            b = b.next
        return dummy.next
```
:::

![82/83. Remove Duplicates from Sorted List I/II](~@assets/lc-82.png#center)


