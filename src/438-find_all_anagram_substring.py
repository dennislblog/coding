class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # just use a sliding window 
        np, ns = len(p), len(s)
        res = []
        if np > ns: return []
        map_ = [0] * 26
        
        for i,x in enumerate(p):
            map_[ord(x) - 97] -= 1
            map_[ord(s[i])-97] += 1
            
        for i in range(ns-np+1):
            #  the last index to check is ns-np
            if not any(map_):
                res.append(i)
            # kick out s[i] and add s[i+np]
            if i + np < ns:
                map_[ord(s[i])-97] -= 1
                map_[ord(s[i+np])-97] += 1
        
        return res