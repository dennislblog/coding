class Solution(object):
    
    def removeKdigits(self, num, k):
        """
        :type num: str
        :type k: int
        :rtype: str

            @ 问题： 去掉(k)个数字，使得剩下的数最小
            @ solution: 用一个stack维护升序数列, 同时update k (k-- when pop out)
            @ example: [1,2,3,7,8,4,5], k = 4
            ---------------------------------------------------------------
            pointer at @           stack(increase)              k
            8                          [1,2,3,7,8]              4
            4                            [1,2,3,4]              2
            5                          [1,2,3,4,5]              2
            最后再pop两次，得到结果[1,2,3], 注意开头是0的情况
        """
        if k == len(num):
            return '0'
        stack = []
        for n in num:
            while k and stack and n < stack[-1]:
                stack.pop()
                k -= 1
            stack.append(n)
        for i in range(k):
            stack.pop()
        return ''.join(stack).lstrip('0') or '0'