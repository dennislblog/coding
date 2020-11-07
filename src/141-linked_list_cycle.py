class Solution(object):
    def detectCycle(self, head):
        """
        :type head: ListNode
        :rtype: ListNode

             @ example: [3,2,0,-4] (-4 ==> 2) 所以返回TRUE，有环
            ---------------------------------------------------
            slow               fast              
            3                  3
            2                  0
            0                  2
           -4                 -4 (now create a new pointer at head)
        """
        # 1. 找到是否有环和快慢相交的地方
        # 2. 从头部重新开始，直到再次相遇(两个慢指针)
        slow = fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if slow == fast:
                cur = head
                while cur != slow:
                    cur = cur.next
                    slow = slow.next
                return cur
        return None1