class Solution:
    """
    问题一： 计算 "(1+(4+5+2)-3)+(6+8)"   只有 加减法 和 括号
    问题二： 计算 "- 3+5 / 2 "            只有 加减法 和 乘除法
    问题三： 计算 "- 3+5 / 2 "            既有加减乘除法又有括号
    问题四： 计算 "e + 8 - a + 5" with {e: 1}   要替换 e = 5, 得到多项式 14 - a 即 ["-1*a","14"]
    """
    def calculate(self, s: str) -> int:
        """
        第二题：
        -------------------------------
        for x in s = - 3+5 / 2 +:
            x -> +:  op = '-', stack = [-3]
            x -> /:  op = '+', stack = [-3, 5]
            x -> +:  op = '/', stack = [-3, 2]
        """
        stack = []
        cur, op = 0, '+'
        for x in s + '+':
            if x == ' ':
                continue
            if x.isdigit():
                cur = cur * 10 + int(x)
            else:
                if op == '+':   stack.append(cur)
                elif op == '-': stack.append(-cur)
                elif op == '/': stack.append(int(stack.pop()/cur))
                else:           stack.append(stack.pop()*cur)
                cur, op = 0, x
        return sum(stack)
                
    class Solution:
    def calculate(self, s: str) -> int:
        """
        第一题：
            num 处理空格间隔开的数; res 是最终结果和括号前面的
        --------------------------------------------------
        for x in s = "-3 - (14+1-16) - (-(12)-(1+2))":
            x -> (:  stack=[-3, -1], res =   0, num =  0
            x -> 6:  stack=[-3, -1], res =  -1, num = 16
            x -> ):  stack=[]      , res = -1*-1 + -3 = -2, num = 0
            x -> (:  stack=[-2, -1], res =   0, num = 0
            
                x -> (:  stack=[-2,-1,0,-1]  
                x -> ):  stack=[-2,-1], res = -12
                
                x -> (:  stack=[-2,-1,-12,-1] 
                x -> ):  stack=[-2,-1], res = -15

            x -> ):  stack=[], res = -15 * -1 - 2 = -13
        """
        res, sign, num = 0, 1, 0
        stack = []
        for x in s + "+":
            if x == ' ': continue
            if x.isdigit():
                num = num * 10 + int(x)
            elif x in '+-':
                res += sign * num; num = 0
                sign = 1 if x == '+' else -1
            elif x == '(':
                stack.append(res)
                stack.append(sign)
                res, sign = 0, 1
            elif x == ')':
                res += sign * num; num = 0
                res = stack.pop() * res + stack.pop()
        return res