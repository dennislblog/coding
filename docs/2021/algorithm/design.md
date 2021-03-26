---
title: 设计题
date: 2021-02-08
categories:
   - Practice
tags:
   - Leetcode
---

<big>栈的应用</big>
::: right
📝 数据结构考点
:::

::::: tabs type: card
:::: tab 迭代器最后一个元素 
## 284. Peeking Iterator

__问题__： 在普通的迭代器类Iterator的基础上增加了peek的功能，就是返回查看下一个值的功能，但是不移动指针，next()函数才会移动指针

::: details
这道题的难点在于如何不调用`next`就能知道`iterator`的下一个元素呢? 可以定义一个变量专门来保存下一个值(相当于提前`pop`), 如果下面还有值的话.

```python
class PeekingIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self._next = iterator.next()

    def peek(self):
        return self._next
        
    def next(self):
        ret = self._next
        if self.iterator.hasNext():
            self._next = self.iterator.next()
        else:
            self._next = None
        return ret

    def hasNext(self):
        return self._next != None
```
:::

```
假设迭代器被初始化为列表 [1,2,3]。

调用 next() 返回 1，得到列表中的第一个元素。
现在调用 peek() 返回 2，下一个元素。 在此之后调用 next() 仍然返回 2。
最后一次调用 next() 返回 3，末尾元素。 在此之后调用 hasNext() 应该返回 False。
```
::::
:::: tab 按频率出栈
## 895. Maximum Frequency Stack

__问题__： 设计一个按照元素出现频率出栈的栈, 当两个元素频率相同时, 后入先出

::: details
- 用`max_cnt`维持当前最大频率, 
- 然后频率等于`max_cnt`的元素相继出栈(按入栈顺序)
- 另外用一个`cnt`字典来跟踪每个元素当前的频率, 如果`cnt2num[max_cnt]`这个list里再也没有元素了, 说明这个频率的都出栈了, 此时`max_cnt -= 1`

```python
"""用优先队列的办法行不通, 是因为每次泵出一个, 队列相关的元素优先级要做出相应改变, 这个并不在priorityQueue的API里?
max := 3
cnt := {5: 3, 7: 2, 4: 1}
cnt2num 
    1: [5, 7, 4]
    2: [5, 7]
    3: [5]
"""
def __init__(self):
    self.cnt = collections.defaultdict(int)
    self.max_cnt = 0
    self.cnt2num = collections.defaultdict(list)

def push(self, x: int) -> None:
    self.cnt[x] += 1
    self.max_cnt = max(self.max_cnt, self.cnt[x])
    self.cnt2num[self.cnt[x]].append(x)
        

def pop(self) -> int:
    ans = self.cnt2num[self.max_cnt].pop()
    self.cnt[ans] -= 1
    if not self.cnt2num[self.max_cnt]:
        self.max_cnt -= 1
    return ans
```
:::
![](~@assets/lc-895.png#center)
::::
:::: tab 中序遍历迭代器
## 173. Binary Search Tree Iterator
**问题**：写一个中序遍历的迭代器, 要求存储空间不得超过 log(n) 平摊访问时间不超过 O(1)
::: details
最简单的方法是一次性按`inorder`逆向压入所有节点, 但这样存储空间是O(n)，不符合要求。 均摊的思想就是每pop一个左子节点，把这个节点右子树的所有左边节点压入栈中
```python                            
class BSTIterator:

    def __init__(self, root: TreeNode):
        self.stack = [] #max size = height of the tree
        self.addleft(root)

    def addleft(self, root: TreeNode):
        while root:
            self.stack.append(root)
            root = root.left
        
    def next(self) -> int:
        out = self.stack.pop()
        self.addleft(out.right)
        return out.val

    def hasNext(self) -> bool:
        return bool(self.stack)
```
:::

![173. Binary Search Tree Iterator](~@assets/lc-173.png#center)
::::
:::::

---

<big>逆向思维</big>
::: right
📝 反着规则去做
:::

::::: tabs type: card
:::: tab 坏的计算器
## 991. Broken Calculator

**问题**: 把$X$通过两种运算变成$Y$, 只能执行 1) 乘以2； 2) 减去1

__例子__: 例如$X = 2, Y = 3$， 我们有 $2 \rightarrow 4 \rightarrow 3$ 两步, 返回答案$2$

::: details
要让$X$做乘2或者减1尽可能接近$Y$, 反过来就是$Y$尽量多的除以2, 直到$Y$比$X$还小的时候, 就只能不断加1得到$X$
```python
def brokenCalc(self, X: int, Y: int) -> int:
    res = 0
    while Y > X:
        if Y % 2 == 0:  Y = Y >> 1  #Y是偶数
        else:               Y = Y + 1   #Y是奇数
        res += 1
    return res + (X-Y)
```
:::
::::
:::: tab set应用
## 575. Distribute Candies

__问题__： 把糖(list of type)分成两堆, 其中一堆种类最多可以有多少

__例子__： candyType = $[6,6,6,6,6,4]$, 返回$2$ 

```python
"""
1. 如果糖的种类 < 糖个数的一半 ===> 每种一个糖都不够一半
2. 如果糖的种类 > 糖个数的一半 ===> 不管怎么分, 一半凑不齐所有种类
"""
def distributeCandies(self, candyType: List[int]) -> int:
    n = len(candyType); distinct = set(candyType)
    return min(n//2, len(distinct))
```
:::::

---

<big>位运算</big>
::: right
📝 位运算规则, $1 << n$相当于$2^n$, $3 << n$相当于$3 \times 2^n$, $n >> 1$相当于$n / 2$
:::

::::: tabs type: card
:::: tab 除法
## 29. Divide Two Integers

__问题__： 计算两个数相除的商，但是不能使用乘法，除法和取余

::: details
```python
"""举例： 25 / 2
while 25 >= 2:
    while 25 >= (2 << 3)
    res += (1 << 3); dividend = 25 - 16 = 9
    while 9 >= (2 << 2)
    res += (1 << 2); dividend = 9 - 8 = 1
所以 res = 8 + 4 = 12
"""
def divide(self, dividend: int, divisor: int) -> int:
    if dividend == 0: return 0
    negative = False
    if (dividend < 0) ^ (divisor < 0): negative = True
    dividend, divisor = abs(dividend), abs(divisor)
    res = 0 
    while dividend >= divisor:
        n = 0
        while dividend >= (divisor << n):
            n += 1
        n = n - 1
        res += (1 << n); dividend -= (divisor << n)
    res = -res if negative else res
    if res < -(1 << 31) or res > (1 << 31) -1:
        return (1 << 31) -1
    return res
```
:::
::::
:::: tab 字符二进制
## 1461. Check If a String Contains All Binary Codes of Size K

__问题__： 如果所有长度为$k$的二进制字符串都是$s$的子串, 返回 True ，否则返回 False

__例子__： `s = "0110", k = 2`, 答案是False, 因为虽然`"01","10","11"`都有包括但是, `"00"`没有包含在里面

::: details
直接把所有长度为$k$的子字符串加到一个集合中, 然后统计所有不同的子串数目是否有$2^K$个
```python
def hasAllCodes(self, s: str, k: int) -> bool:
    S = set(); n = len(s)
    for i in range(n-k+1):
        S.add(s[i:i+k])
    return len(S) == 2**k
```
:::
::::
:::::

---

<big>哈希表</big>
::: right
📝 数据结构
:::

::::: tabs type: card
:::: tab 哈希集
## 705. Design HashSet
__问题__： 动手实现一个`HashSet`. 不能用已经内置的函数

::: details
创建一个二维数组, 第一个维度存取hash, 第二个维度保存具体元素
```python
"""
obj = MyHashSet()
obj.add(1000000)
obj.remove(1000000)
param_3 = obj.contains(1000000) # return False
"""
class MyHashSet:

    def __init__(self):
        self.buckets = 1000
        self.itemsPerBucket = 1001 #overall ele <= 1e6
        self.table = [[] for _ in range(self.buckets+1)]
        self.find = lambda key: divmod(key, self.buckets)
        
    def add(self, key: int) -> None:
        hashkey, pos = self.find(key)
        if not self.table[hashkey]:
            self.table[hashkey] = [0] * self.itemsPerBucket
        self.table[hashkey][pos] = 1

    def remove(self, key: int) -> None:
        hashkey, pos = self.find(key)
        if self.table[hashkey]:
            self.table[hashkey][pos] = 0

    def contains(self, key: int) -> bool:
        hashkey, pos = self.find(key)
        return (self.table[hashkey] != []) and (self.table[hashkey][pos] == 1)
```
:::
::::
:::: tab 哈希表
## 706. Design HashMap
__问题__： 动手实现一个`HashMap`. 不能用已经内置的函数
::: details
创建一个二维数组, 第一个维度存取hash, 第二个维度保存具体元素, 跟$705$一样, 只是存具体的值, 而不是`0/1`, 这里值的范围是$[0,1e6]$
```python
"""
obj = MyHashSet()
obj.put(2, 1)
obj.remove(2)
param_3 = obj.contains(2) # return False
"""
class MyHashMap:

    def __init__(self):
        bucket, self.itemsPerBucket = 1001, 1001
        self.table = [[] for _ in range(bucket)]
        self.find = lambda key: divmod(key, bucket)

    def put(self, key: int, value: int) -> None:
        key, pos = self.find(key)
        if not self.table[key]:
            self.table[key] = [-1] * self.itemsPerBucket
        self.table[key][pos] = value

    def get(self, key: int) -> int:
        key, pos = self.find(key)
        if self.table[key] != [] and self.table[key][pos] != -1:
            return self.table[key][pos]
        return -1

    def remove(self, key: int) -> None:
        key, pos = self.find(key)
        if self.table[key]:
            self.table[key][pos] = -1
```
:::
::::
![](~@assets/lc-705.png#center)
:::: tab 设计地铁打票
__问题__：请你实现一个类 UndergroundSystem, 实现`1. checkIn(id, start_station, time)`, 以及`2. checkOut(id, end_station, t)`, 以及`getAverageTime(start, end)`计算所有从始发站到终点站的平均花费时间. 

::: details
最后我需要一个存储`key = (start, end), value = time duration`的字典, 而`checkout输入只包含了 end_station 和 end_time`, 所以自然我需要另一个字典根据`id`记录`start_station 和 start_time`
```python
# obj = UndergroundSystem()
# obj.checkIn(id,stationName,t)
# obj.checkOut(id,stationName,t)
# param_3 = obj.getAverageTime(startStation,endStation)

def __init__(self):
    self.psg = dict()
    self.time = collections.defaultdict(list)

def checkIn(self, id: int, stationName: str, t: int) -> None:
    self.psg[id] = (stationName, t)

def checkOut(self, id: int, stationName: str, t: int) -> None:
    start, t0 = self.psg[id]
    self.time[(start, stationName)].append(t - t0)

def getAverageTime(self, startStation: str, endStation: str) -> float:
    times = self.time[(startStation, endStation)]
    return sum(times)/len(times)
```
:::
::::
:::::

---

## 535. Encode and Decode TinyURL

:::: tip
__问题__： 这个题是个佛性题, 不给任何要求, 只要能编码/解码就行, 比如
```python
codec = Codec()
input = "https://leetcode.com/problems/design-tinyurl"
encode = codec.encode(input)
# >> return a short url, for example, http://tinyurl.com/0
decode = codec.decode(encode)
# >> return original input "https://leetcode.com/problems/design-tinyurl"
```

::: details
做法很简单, 设计一个数组, 对每一个输入给与一个单独的编码即可, 注意字符串的处理即可
```python
class Codec:
    urls = []
    def encode(self, longUrl: str) -> str:
        self.urls.append(longUrl)
        return "http://tinyurl.com/" + str(len(self.urls)-1)
    def decode(self, shortUrl: str) -> str:
        return self.urls[int(shortUrl.split('/')[-1])]
```
:::
::::

---

<big>字符串</big>
::: right
📝 字符串的一些题目总结
:::

## 966. Vowel Spellchecker

:::: tip
__问题__： 现在给了一个单词字典，给出了一堆要查询的词，要返回查询结果。查询的功能如下：

1. 如果字典里有现在的单词，就直接返回；
2. 如果不满足1，那么判断能不能更改要查询单词的某些大小写使得结果在字典中，如果字典里多个满足条件的，就返回第一个；
3. 如果不满足2，那么判断能不能替换要查询单词的元音字符成其他的字符使得结果在字典中，如果字典里多个满足条件的，就返回第一个；
4. 如果不满足3，返回查询的结果是空字符串。

__例子__： 返回`wordlist`里的内容
```
Input: 
    wordlist = ["KiTe","kite","hare","Hare"], 
    queries = ["kite","Kite","KiTe","Hare","HARE","Hear","hear","keti","keet","keto"]

Output:
    ["kite","KiTe","KiTe","Hare","hare","","","KiTe","","KiTe"]
```

::: details
- 首先，判断有没有相同的单词，这个很好办，直接使用set
- 把字符转换为全部小写, 看是否在`wordlist`里有对应的单词, 要注意由于需要返回原`wordlist`中的单词, 且优先返回第一个出现的, 因此我们在建立`小写->原单词`的字典时, 从后往前扫描, 因为可能出现两个单词小写化后一模一样
- 最后是元音转换, 把所有元音都换成符号`#`, 同样也是从后往前, 因为要返回原`wordlist`中第一个匹配的

```python
def spellchecker(self, wordlist: List[str], queries: List[str]) -> List[str]:
    wordset = set(wordlist); res = []
    wordmap = {w.lower(): w for w in wordlist[::-1]}
    vowelmap = {re.sub("[aeiou]","#",w.lower()): w for w in wordlist[::-1]}
    for q in queries:
        if q in wordset:
            res.append(q)
        else:
            q = q.lower()
            if q in wordmap:
                res.append(wordmap[q])
            else:
                q = re.sub("[aeiou]","#",q.lower())
                if q in vowelmap:
                    res.append(vowelmap[q])
                else:
                    res.append("")
    return res
```
:::
::::


