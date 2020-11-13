class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode

            @ 问题:        (7 -> 2 -> 4 -> 3) 
                        +       (5 -> 6 -> 4)
                        =  (7 -> 8 -> 0 -> 7)
            @ solution: 先用stack，倒序存储求和，然后从最后往前面append节点
            ------------------------------------------------------------
            operation                current               previous              
            divmod(3+4) = 0, 7       ListNode(7)           ListNode(0)
            divmod(4+6) = 1, 0       ListNode(0)           ListNode(1)
            divmod(2+5+1) = 0, 8     ListNode(8)           ListNode(0)
            divmod(7) = 0, 7         ListNode(7)           ListNode(0)
        """
        
        s1, s2 = [], []
        while l1:
            s1.append(l1.val)
            l1 = l1.next
        while l2:
            s2.append(l2.val)
            l2 = l2.next
        
        cur = ListNode(0)
        while s1 or s2:
            tmp = cur.val
            if s1:
                tmp += s1.pop()
            if s2:
                tmp += s2.pop()
            a, b = divmod(tmp, 10)
            cur.val, pre = b, ListNode(a)
            pre.next = cur
            cur = pre
        
        # in case 19 + 81 => 100
        if cur.val:
            return cur
        else:
            return cur.next