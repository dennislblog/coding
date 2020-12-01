class Solution:
    """
    @问题： 
        A = [[0,2],[5,10],[13,23],[24,25]]
        B = [[1,5],[8,12],[15,24],[25,26]]
        求 A ∩ B = [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
    @思路： 
        1) 和mergesort的merge step很像
        2) 先确定当前两个指针所在的 interval a 和 interval b 有交集
        3) 确定交集后，移动相应指针
    """
    def intervalIntersection(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        nA, nB = len(A), len(B)
        res = []
        i, j =  0, 0
        while i < nA and j < nB:
            if A[i][0] > B[j][1]:
                j += 1
            elif A[i][1] < B[j][0]:
                i += 1
            else:
                # A and B have overlaps
                left  = max(A[i][0], B[j][0])
                right = min(A[i][1], B[j][1])
                res.append([left, right])
                if right == A[i][1]:
                    i += 1
                else:
                    j += 1
        return res