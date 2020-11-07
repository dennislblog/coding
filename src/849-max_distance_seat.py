class Solution(object):
    def maxDistToClosest(self, seats):
        """
        :type seats: List[int]
        :rtype: int
        @ 问题：maximum distance to the closest person.

            @ example: [1,0,0,0,1,0,1]  ==> return 2 坐在index=2,离两边各2个位置
            -------------------------------------------------------------------
            i (seats[i] == 1)          start                res
            0                          0                    (0 - 0)
            4                          5                    (4+1-0)/2
            6                          7                    
        """
        # 1. 从左到右扫描，一旦遇到有人，开始统计，并从下一个index重新计算
        # 2. 考虑两个特殊情况，1) 第一次遇到seat; 2) 从最后seat到最后
        res, start = 0, 0
        n = len(seats)
        for i in range(n):
            if seats[i] == 1:
                if start == 0:
                    res = i - start
                else:
                    res = max(res, (i-start+1)//2)
                start = i+1
        return max(res, (n-start))er