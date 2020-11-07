class Solution(object):
    def champagneTower(self, poured, query_row, query_glass):
        """
        :type poured: int
        :type query_row: int
        :type query_glass: int
        :rtype: float
        @ now suppose pour = 2, row = 1, glass = 1
        """
        # 暴力解法吧，逐级往下倒，一直倒到query_row行, 然后和 (1) 溢杯
        q = [float(poured)]
        for i in range(query_row):
            q2 = [0] * (i+1+1)
            for j, each in enumerate(q):
                if each > 1:
                    left = (each-1)/2 
                    q2[j] += left
                    q2[j+1] += left
            q = q2
        return min(q[query_glass], 1)7.82