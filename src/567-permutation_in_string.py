class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # check if s2 contains permutation of s1
        n1, n2 = len(s1), len(s2)
        if n1 > n2: return False
        map_ = [0] * 26
        for i in range(n1):
            idx1, idx2 = ord(s1[i]), ord(s2[i])
            map_[idx1-97] -= 1
            map_[idx2-97] += 1
        for i in range(n2-n1+1):
            if not any(map_):
                return True
            map_[ord(s2[i])-97] -= 1
            if i + n1 < n2:
                map_[ord(s2[i+n1])-97] += 1 
        return False