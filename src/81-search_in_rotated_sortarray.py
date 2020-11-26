class Solution:
    """
        @问题： 在一个排序数列中(rotate一次所以一定是 a < ... < b > c ... < d and d < a 所以是先升再突然下降再继续升，但不超过一开始那个)
        @解法： 二分法，两点需要注意：   
                    1) 通过判断mid与right判断哪一边一定是升序； 
                    2) [1,1,3,1] 和 [3,1,1] 这两种特殊情况，当 mid = right时，哪边都有可能是升序，这个时候 right -= 1 (和154题一模一样)
        -----------------------------------------------------------------
        $ 例子 [2,5,5,5,0,1,2] 寻找 2
        ----------------------
        iter       i       j      k      mid vs. right        which side         target(2) in ↗ ?
        1          0       6      3      5   vs. 2            left[2,5]  ↗       yes ==> j = k-1 = 2
        2          0       2      1      5   vs. 5            can't decide       j = j-1 = 1
        3          0       1      0 (return True since nums[k] == target)   

    """
    def search(self, nums: List[int], target: int) -> bool:
        i, j = 0, len(nums) - 1
        while i < j:
            k = (i + j) >> 1
            if nums[k] == target:
                return True
            left, right, mid = nums[i], nums[j], nums[k]
            if mid < right:
                if mid <= target <= right:
                    i = k + 1
                else:
                    j = k
            elif mid > right:
                if left <= target <= mid:
                    j = k
                else:
                    i = k + 1
            else:
                j -= 1
            # print("i={}, j={}, k={}, l={}, r={}, mid={}".format(i,j,k, left,right,mid))
        return nums != [] and nums[i] == target