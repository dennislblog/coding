---
title: 设计题
date: 2021-02-08
categories:
   - Practice
tags:
   - Leetcode
---

<big>栈/队列的应用</big>
::: right
📝 数据结构考点
:::

::::: tip 
:::: tabs type: card
::: tab 迭代器最后一个元素 
## 284. Peeking Iterator

__问题__： 在普通的迭代器类Iterator的基础上增加了peek的功能，就是返回查看下一个值的功能，但是不移动指针，next()函数才会移动指针

```bash
假设迭代器被初始化为列表 [1,2,3]。

调用 next() 返回 1，得到列表中的第一个元素。
现在调用 peek() 返回 2，下一个元素。在此之后调用 next() 仍然返回 2
最后一次调用 next() 返回 3，末尾元素。在此之后调用 hasNext() 应该返回 false。
```

```python
"""主要就是如何在不调用 next() 条件下, 提前保存下一个被调用的值(如果还有的话)
"""
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
::: tab 按频率出栈
## 895. Maximum Frequency Stack

![](~@assets/lc-895.png#right)
> __问题__： 设计一个按照元素出现频率出栈的栈, 当两个元素频率相同时, 后入先出
> - 用`max_cnt`维持当前最大频率, 
> - 然后频率等于`max_cnt`的元素相继出栈(按入栈顺序)
> - 另外用一个`cnt`字典来跟踪每个元素当前的频率, 如果`cnt2num[max_cnt]`这个list里再也没有元素了, 说明这个频率的都出栈了, 此时`max_cnt -= 1`

```bash
输入：
["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"]
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]
输出：[null,null,null,null,null,null,null,5,7,5,4]
解释：
    一系列push操作后, 栈自下而上是[5,7,5,7,4,5]; 接着pop()返回5, 因为5是频率最多的
    栈现在变成[5,7,5,7,4]; 然后pop()返回7, 因为虽然5和7的频率相同, 但7更接近栈顶
```

```python
"""
用优先队列的办法行不通, 是因为每次泵出一个, 队列相关的元素优先级要做出相应改变
max := 3                                # max_cnt 维持当前最高频次
cnt := {5: 3, 7: 2, 4: 1}               # 先从cnt2num最高频率的泵出(先进先出)
cnt2num                                 # cnt统计每个数出现的频次, 用来更新max_cnt和cnt2num
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
::: tab 中序遍历迭代器
## 173. Binary Search Tree Iterator

![173. Binary Search Tree Iterator](~@assets/lc-173.png#small)
> **问题**：写一个中序遍历的迭代器, 要求存储空间不得超过 log(n) 平摊访问时间不超过 O(1)
> - 最简单的方法是一次性按`inorder`逆向压入所有节点, 但这样存储空间是O(n)，不符合要求。 
> - 均摊的思想就是每pop一个左子节点，把这个节点右子树的所有左边节点压入栈中

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
::: tab 循环队列
> ![](~@assets/lc-622.png#right)
> __问题__： 实现一个环形链表, 难点在于如何用有限的内存实现无限滚动(取模的思想)
> - 维持一个头指针和当前容量
> - 如果长度超过$k$, 就满了, 此时不能再添加
> - 如果长度为0, 则代表队列是空的, 如果要泵出(头指针), 然后更新头指针和长度
> - 取头直接调用头指针, 取尾则用`head+size-1%size`

```python
"""题目描述

MyCircularQueue circularQueue = new MyCircularQueue(3); // 设置长度为 3
依次输入(enQueue) 1,2,3 得到 [1,2,3], 此时长度满了, 再输入4, 返回FALSE
circularQueue.Rear()         >> 3
circularQueue.isFull()       >> True
circularQueue.deQueue()      >> True 此时泵出1
circularQueue.enQueue(4)     >> True 此时把4加到3后面, 头指针指向2
circularQueue.Rear()         >> 4
"""
class MyCircularQueue:
    def __init__(self, k: int):
        self.cap = k
        self.head = 0
        self.q = [0] * k
        self.cnt = 0
    def enQueue(self, value: int) -> bool:
        if not self.isFull():
            self.cnt += 1
            self.q[(self.head + self.cnt - 1) %self.cap] = value
            return True
        return False
    def deQueue(self) -> bool:
        if not self.isEmpty():
            self.cnt -= 1
            self.head = (self.head + 1) %self.cap
            return True
        return False
    def Front(self) -> int:
        if self.isEmpty(): return -1
        else:              return self.q[self.head]
    def Rear(self) -> int:
        if self.isEmpty(): return -1
        else:              return self.q[(self.head + self.cnt - 1) %self.cap]
    def isEmpty(self) -> bool:
        return self.cnt == 0
    def isFull(self) -> bool:
        return self.cnt == self.cap
```
:::
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

::: tip
要让$X$做乘2或者减1尽可能接近$Y$, 反过来就是$Y$尽量多的除以2, 直到$Y$比$X$还小的时候, 就只能不断加1得到$X$
:::

```python
def brokenCalc(self, X: int, Y: int) -> int:
    res = 0
    while Y > X:
        if Y % 2 == 0:  Y = Y >> 1  #Y是偶数
        else:               Y = Y + 1   #Y是奇数
        res += 1
    return res + (X-Y)
```
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
::::
:::: tab 戳印序列
## 936. Stamping The Sequence

**问题**: 通过在`????????`上面不断盖戳`stamp`, 使其变成`target`

```bash
输入：stamp = "abca", target = "aabcaca"
输出：[3,0,1]
解释：即首先变成"aababca", 然后在第1个位置盖一个, 变成"abcabca", 最后在第二个位置, 变成"aabcaca"
```
::: tip
逆向思维, 如果`target = ababc`都变成了`target = ?????`就代表成功, 每次从左到右遍历, 如果找不到可以被替换的, 且`target`还不全是`?`的时候, 返回`[]`(没有答案)

注意最后要将答案逆序因为我们是逆向思考, 因为后面盖的章会覆盖前面盖的章
:::

```python
def movesToStamp(self, stamp: str, target: str) -> List[int]:
    def check(i):
        res = 0
        for j in range(n_stm):
            if target[i+j] == '?': 
                continue
            elif target[i+j] == stamp[j]:
                res += 1
            else:
                return 0
        return res
        
    res = []; tot = 0; target = list(target)
    n_stm, n_tar = len(stamp), len(target)
    while tot < n_tar:
        pre_tot = tot
        for i in range(n_tar - n_stm + 1):
            can_replace = check(i)
            if can_replace != 0:
                target[i:i+n_stm] = ['?'] * n_stm
                tot += can_replace; res.append(i)
        if pre_tot == tot: return []
    return res[::-1]
```
::::
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



