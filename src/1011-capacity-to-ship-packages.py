
from typing import List


class Solution:
    def shipWithinDays(self, weights: List[int], D: int) -> int:

        low, high = 0, 0
        for weight in weights:
            high += weight
            low = max(low, weight)

        def test(capacity):
            """return the least days to finish with that capacity
            """
            res = 1
            total = 0
            for weight in weights:
                if total + weight > capacity:
                    res += 1
                    total = weight
                else:
                    total += weight
            return res

        res = high
        days = 1
        while low < high:
            mid = (low + high)//2
            # print("low={},high={},mid={}, res={}, D={}".format(low, high, mid, test(mid), D))
            days = test(mid)
            if test(mid) > D:      # insufficient time, mulow expand capacity
                low = mid + 1
            else:
                res = mid
                high = mid

        return res if days > D else low
