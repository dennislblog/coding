class Solution:
    """
    :type k: int
    :type prices: List[int]
    :rtype: int

            @ solution: 因为单纯买并不构成一次交易（要买完再卖）用DP track f(k, B) 和 f(k, S) 
                        记录截至目前完成（刚好K次）交易条件下且当前状态 Buy 或者 没有 Buy 的最大利润
            @ example: prices = [3，2，6，5，0，3], 最多(k=2)次交易 ==> return 7 (2买入6卖出，0买入3卖出)
            ------------------------------------------------------------------------------------------
            第i天                f(0,B)          f(1,S)          f(1,B)          f(2,S)          f(2,B)      
            2  (price = 2)          -2               0              -2               0              -3
            3  (price = 6)          -2               4              -2               4              -3
            4  (price = 5)          -2               4              -1               4              -3
            5  (price = 0)           0               4               4               4              -3
            5  (price = 3)           0               4               4               7              -3 (我感觉最后这个值是-2？)
    """
    def maxProfit(self, k, prices):
        if not prices: return 0
        n = len(prices)
        
        # If I can buy/sell anywhere I want
        if k > n // 2:
            res = 0
            for i in range(1, len(prices)):
                if prices[i] > prices[i - 1]:
                    res += prices[i] - prices[i - 1]
            return res
        
        """
        f(j, L|H): require long|hold position at the current moement
        with no more than j transactions (1 trans: buy and then sell)
            
        - f(j-1, L) = max( f(j-1,L) ; f(j-1,H) - today price)
        - f(j, H) = max( f(j, H) ; f(j-1, L) + today price)
        """
        n = len(prices)
        f = [[0, 0] for _ in range(k + 1)]
        for i in range(k + 1):
            # this assumes the worst first buy price
            f[i][0] = -prices[0]
        for i in range(1, n):
            for j in range(1, k + 1):
                f[j - 1][0] = max(f[j - 1][0], f[j - 1][1] - prices[i])
                f[j][1] = max(f[j][1], f[j - 1][0] + prices[i])  
        return f[k][1]