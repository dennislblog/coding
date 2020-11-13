class Solution:
    def validSquare(self, p1: List[int], p2: List[int], p3: List[int], p4: List[int]) -> bool:
        def distance(x,y):
            return (x[0]-y[0])**2 + (x[1]-y[1])**2
        lst = [p1,p2,p3,p4]
        cnt = dict()
        for i in range(4):
            for j in range(i):
                dist = distance(lst[i],lst[j])
                cnt[dist] = cnt.get(dist, 0) + 1
        try:
            a,b = cnt.values()
            if min(a,b)==2 and max(a,b)==4:
                return True
            else:
                return False
        except:
            return False