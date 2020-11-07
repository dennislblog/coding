class Solution(object):
    def bagOfTokensScore(self, tokens, P):
        """
        :type tokens: List[int]
        :type P: int
        :rtype: int

            @ solution: 用power买第一个credit, 用一个credit兑换400power，加上之前剩下的100，凑齐500买中间200和300两个credit
            @ example: tokens = [100,200,300,400], Power = 200 ==> return 2 
            ---------------------------------------------------------------
        """
        # 1. 首先排序(最关键)，每次power不足了，用1个token去换最大的power
        # 2. 因为最终是最大化token，所以优先用power去买消耗少的token
        tokens.sort()
        n = len(tokens); i, j = 0, n-1
        score, res = 0, 0
        while i <= j:
            if P >= tokens[i]:
                P -= tokens[i]
                i += 1; score += 1
                # 这一步相当关键，因为有可能score先变小是为了变得更大
                res = max(res, score)
            elif score > 0:
                P += tokens[j]
                j -= 1; score -= 1
            else:
                break
        return res