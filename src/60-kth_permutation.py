class Solution:
    """
        @问题：给定两个数 (n=4, k=15) 找到[1,2,3,4] permutation的第13个
        @solution：从最高位开始计算，后面的n-1位总共有 (n-1)! 种排列组合
                   所以先创建一个 klst = [1,1,2,6,24,120 ...] 即 (n-1)!
                   然后整除，从最小开始取
                   nlst = [1,2,3,4,5,6,7,8,9] 从最小取，并pop出来 O(n)
        -------------------------------------------------------------
        首先 k = k - 1 = 14 
                    k // klst[i]        k % klst[i]         nlst op.
        i = 3       14/6 = 2            14%6 = 2            pop '3'
        i = 2        2/2 = 1             2%2 = 0            pop '2'
        i = 1        0/1 = 0             0%1 = 0            pop '1'
        i = 0                                               pop '4'
        所以答案等于 '3214'
    """
    def getPermutation(self, n: int, k: int) -> str:
        nlst = list("123456789")
        klst = [1] * n
        res = ""
        for i in range(1,n):
            klst[i] = klst[i-1] * i 
            
        k -= 1
        
        for i in range(n-1, -1, -1):
            ind, k = divmod(k, klst[i])  
            cur = nlst.pop(ind)
            res += str(cur)
        return res