class Solution:
    """
        @ 问题： 就是拆解braces, s is guaranteed to be a valid input.
        @ 例子： input s = "3[a]2[bc]", output = "aaabcbc" 把[a]复制了3遍，然后[bc]复制了2遍
        @ 思路： 分情况处理， 遇到'['代表要把 '[]' 前面的 int 和 str 暂时保存
                            遇到']'代表要把 '[]' 前面的数字和当前 str 结合 
                            遇到数字，更新 int   遇到字符，更新str
        ------------------------------------------------------------
        s = "1[f3[v]02[fd]]"
        cur             int             str             stack
        ---             ---             ---             -----
        1               '1'             ''              []
        [               ''              ''              ['', 1]
        [               ''              ''              ['', 1, 'f', 3]
        ]               ''              'fvvvv'         ['', 1]
        [               ''              ''              ['', 1, 'fvvv', 2]   #在这一步，
        ]               ''              'fvvvfdfd'      ['', 1]
        ]               ''              'fvvvfdfd'      []
    """
    def decodeString(self, s: str) -> str:
        stack = []
        cur_num = cur_str = ''
        for c in s:
            if c == '[':
                stack.append(cur_str)
                stack.append(int(cur_num))
                cur_num = cur_str = ''
            elif c == ']':
                num = stack.pop()
                prev_str = stack.pop()
                cur_str = prev_str + cur_str * num
            elif c.isdigit():
                cur_num += c
            else:
                cur_str += c
        return cur_str
        