class Solution:
    """
    @问题： 在 linked list 1 -> 2 -> 3 中，call self.geRandom() 返回任意一个node的value
    @思路： 要求不能使用额外空间, 并且无法统计链表长度，于是答案有个蓄水池法

    蓄水池
        cur @1   res = 1 的概率暂时是 1                               cnt++
        cur @2   res = 2 的概率为1/2, 即 res != 1 的概率变成了1/2      cnt++
        cur @3   res = 3 的概率为1/3, 
                        还是 res = 1 的概率是1x(1-1/2)x(1-1/3)=1/3 
                        还是 res = 2 的概率是1/2 x (1-1/3) = 1/3

    这方法太牛逼了
    """
    def __init__(self, head: ListNode):
        """
        @param head The linked list's head.
        Note that the head is guaranteed to be not null, so it contains at least one node.
        """
        self.head = head
        
    def getRandom(self) -> int:
        """
        Returns a random node's value.
        """
        cur, cnt = self.head, 0
        while cur:
            if random.randint(0, cnt) == 0:
                res = cur.val
            cur = cur.next
            cnt += 1
        return res


    """
    @类似： 第398题, 在一个有重复项的数列中, 随机返回 target number 的 index
    @思路： 
        时间换空间: 可以选择遍历数列, 把所有 val=target 的 index 全部存起来, 然后随机选一个
        空间换时间: 不选择遍历, 而是一开始用字典把所有 val->index 的映射建立, 然后随机选一个
        蓄水池疗法: 跟上面一样, 每次碰到 target, cnt++, 答案按照 1/cnt 概率被更新
    """
    def __init__(self, nums: List[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        cnt = 0
        for ind, num in enumerate(self.nums):
            if num == target:
                if random.randint(0, cnt) == 0:
                    res = ind
                cnt += 1
        return res
