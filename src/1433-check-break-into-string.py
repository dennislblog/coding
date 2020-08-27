from typing import List

class Solution:
    def checkIfCanBreak(self, s1: str, s2: str) -> bool:
        cnt1 = collections.Counter(s1)
        cnt2 = collections.Counter(s2)
        diff = 0
        win1, win2 = False, False
        for ch in string.ascii_lowercase:
            diff += cnt1[ch] - cnt2[ch]
            win2 |= (diff > 0)
            win1 |= (diff < 0)
        return not (win1 & win2)