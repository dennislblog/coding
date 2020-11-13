class Solution:
    def oddEvenList(self, head: ListNode) -> ListNode:
        cnt = 1
        odd, even = ListNode(0), ListNode(0)
        firsteven = even
        cur = ListNode(0, head)
        while cur.next:
            cur = cur.next
            if cnt%2:
                odd.next = cur
                odd = odd.next
            else:
                even.next = cur
                even = even.next
            cnt += 1
        #
        # 1. break the even from the last odd
        # 2. connect odd to first even
        #
        even.next = None
        odd.next = firsteven.next
        
        return head