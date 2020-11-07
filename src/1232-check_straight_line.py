class Solution(object):
    def checkStraightLine(self, coordinates):
        """
        :type coordinates: List[List[int]]
        :rtype: bool
        @ 问题： 判断是否是一条直线
        """
        # 直接看 d(y-y0) * d(x1-x0) == d(x-x0) * d(y1-y0)
        dy = coordinates[1][1] - coordinates[0][1]
        dx = coordinates[1][0] - coordinates[0][0]
        for i in range(2, len(coordinates)):
            dyp = coordinates[i][1] - coordinates[0][1]
            dxp = coordinates[i][0] - coordinates[0][0]
            if dy * dxp != dx * dyp:
                return False
        return True0:13.36