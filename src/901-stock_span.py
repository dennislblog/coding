class StockSpanner:
	"""
	>> S = StockSpanner()
	>> S.next(100)  ==> return 1
	>> S.next(80)   ==> return 1
	...
	>> S.next(75)   ==> return 4

        @ 问题：把 price 依次放进去，每次告诉我在他(consecutive front)前面有多少个不比他大
	    @ example: prices = [100, 80, 60, 70, 60, 75, 85] ==> 依次返回 [1,1,1,2,1,4,6]
        -----------------------------------------------------------------------------
        pointer 				stack                                 event
        100						[(100,1)]                             append
        80 						[(100,1), (80,1)]				      append
        60                      [(100,1), (80,1), (60,1)]			  append
        70                      [(100,1), (80,1), (70,2)]       	  res += (60,1).pop()
	"""

    def __init__(self):
        # use a dec. stack to track (number, index) latest appearnce
        self.stack = []
        

    def next(self, price: int) -> int:        
        res = 1
        while self.stack and price >= self.stack[-1][0]:
            res += self.stack.pop()[1]
        self.stack.append((price, res))
        return res