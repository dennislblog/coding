class Solution:
    """
    @问题： 在 nums = [2,2,1,1,1,2,2] 中找出 majority elements 即出现次数大于一半的数字，这里答案是 2
    @思路：  1)如果用字典计数，那么时空间复杂度都是o(n) 
         :  2)用摩尔投票法 Moore Voting，用一个cnt计算某一个元素相比所有其他元素的势能，选那个势能最大的
    """
    def majorityElement(self, nums: List[int]) -> int:

        res, cnt = nums[0], 0
        for num in nums:
            if num == res:
                cnt += 1
            else:
                cnt -= 1
                if cnt == 0:
                    res, cnt = num, 1
        return res

    """
    @相关： 第 229 题，要求找出所有出现频率大于 n/3 的
    @思路： 用两个变量，统计最多和次多元素的势能，然后分别统计这两个元素出现次数，最后和 n/3 比较
    -------------------------------------------------------------------------------------
    @例子： nums = [1,2,3,1]
    -----------------------
    cur@      [x,y]        [cx,cy]
    1         [1,2]        [ 1,0 ]
    2         [1,2]        [ 1,1 ]
    3         [1,2]        [ 0,0 ]
    1         [1,2]        [ 1,0 ]
    """
    def majorityElement(self, nums: List[int]) -> List[int]:

        res, cx, cy = [], 0, 0
        n = len(nums)
        if n == 1:
            return nums
        x, y = nums[0], nums[1]
        for num in nums:
            if   num == x:    cx += 1
            elif num == y:    cy += 1
            elif cx  == 0:    x = num; cx = 1
            elif cy  == 0:    y = num; cy = 1
            else:             cx -= 1; cy -= 1
        cx, cy = 0, 0
        for num in nums:
            if   num == x:    cx += 1
            elif num == y:    cy += 1
        if cx > n/3:          res.append(x)
        if cy > n/3:          res.append(y)
        return res