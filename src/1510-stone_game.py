class Solution(object):
    def winnerSquareGame(self, n):
        """
        :type n: int
        :rtype: bool

            @ solution: DP to track whether Bob win if initial number is n
            @ example: n = 5, you go first and then Bob, 每次挑选 i^2 个
            -----------------------------------------------------------
            i = ?               BobWin
            1:                  [True, False, True, True, True, True] (i > 1 doens't heave any meaning)
            2:                  [True, False, True, True, True, True] (i == 2, no matter what you do, Bob would definitely win)
            3:                  [True, False, True, False, True, True]
            4:                  [True, False, True, False, False, True]
            5:                  [True, False, True, False, False, True]
        """
        # 动态规划：比如`n=10`, 只需要看(10-1),(10-4)(10-9)有没有False
        # 只要有一个False，代表Bob最优处理下可以win, 那么Alice可以通过一个额外的j^2操作实现逆袭
        BobWin = [True] * (1+n)
        
        for i in range(1, n+1):
            j = 1
            while j * j <= i:
                if BobWin[i - j*j]:
                    BobWin[i] = False
                    break
                j += 1
        return not BobWin[n]
