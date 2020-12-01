class Solution:
    """
    @问题：这道题像是一道sliding window的题，但他要求子序列每一个字符都在 `子序列` 中出现至少 k 次
    @思路：分治法，Count每个字符出现的次数，如果某个字符不足k次，踢掉，两边分别计算结果
    ----------------------------------------------------------------------------
    例如 s = "ababbc" k = 3
    -----------------------
    首先Count "ababbc" ==> {'a': 2, 'b': 3, 'c': 1}
    遍历      "ababbc" ==> cnt[a] < k, rtrn max(a左边, a右边)
    --------------------------------------------------------
    左边子序为空，长度小于 k, rtrn 0
    右边子序  "babbc"
    首先Count "babbc" ==> {'a': 1, 'b': 3, 'c': 1}
    遍历      "babbc" ==> cnt[a] < k, rtrn max(a左边, a右边)
    --------------------------------------------------------
    左边子序为'b'，长度小于 k, rtrn 0
    右边子序  "bbc"
    首先Count "bbc" ==> {''b': 2, 'c': 1}
    遍历      "bbc" ==> cnt[b] < k, rtrn max(b左边, b右边) -> 左右长度都小于k，返回0

    PS： 每一次子序都得重新计数吗？
    """ 
    def longestSubstring(self, s: str, k: int) -> int:
        n = len(s)
        
        def helper(start, end):
            if end - start < k: return 0
            cnt = [0] * 26
            for i in range(start, end):
                cnt[ord(s[i]) - 97] += 1
            for i in range(start, end):
                if cnt[ord(s[i]) - 97] < k:
                    return max(helper(start, i), helper(i+1, end))
            return end - start
            
        return helper(0, n)