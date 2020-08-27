from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # backtracking
        res = []
        candidates.sort()
        n = len(candidates)

        def backtrack(out, osum, st):
            if osum > target:
                return  # backtracking
            if osum == target:
                res.append(out[:])
                return
            for i in range(st, n):
                out.append(candidates[i])
                backtrack(out, osum+candidates[i], i)
                out.pop()
        backtrack([], 0, 0)
        return res
