class Solution(object):
    def insertionSortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        
        @ example: [-1, 5, 3, 4, 0]
            -----------------------
            first      [-1,3,5,4,0]
            second     [-1,3,4,5,0]
            third      [-1,0,3,4,5]
        """
        dummy = ListNode(-999) 
        pre = dummy
        while head:
            cur = head
            head = head.next
            # 下面两行偷懒，pre是上一个操作插入的位置
            if cur.val < pre.val:
                pre = dummy
            # 找到cur.val可以插入的地方
            while pre.next and pre.next.val < cur.val:
                pre = pre.next
            # 插入cur.val
            cur.next, pre.next = pre.next, cur
            # 这一步更新尤其重要
            pre = cur
        return dummy.next        