from typing import List


class TreeNode(object):
    def __init__(self, start, end):
        self.left = self.right = None
        self.start = start 
        self.end = end

    def insert(self, news, newe):
        if news >= self.end:
            if not self.right:
                self.right = TreeNode(news, newe)
                return True
            return self.right.insert(news, newe)
        
        elif newe <= self.start:
            if not self.left:
                self.left = TreeNode(news, newe)
                return True
            return self.left.insert(news, newe)
        
        else:
            return False

class MyCalendar(object):
    def __init__(self):
        self.root = None

    def book(self, start, end):
        if self.root is None:
            self.root = TreeNode(start, end)
            return True
        return self.root.insert(start, end)

# Your MyCalendar object will be instantiated and called as such:
# obj = MyCalendar()
# obj.book(10, 20)  --> True
# obj.book(15, 25)  --> False
# obj.book(20, 25)  --> True