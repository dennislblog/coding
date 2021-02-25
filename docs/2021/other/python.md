---
title: Python技巧
date: 2021-01-15
autoGroup-3: 知识 
categories:
  - Knowledge
tags:
  - Python
sidebarDepth: 3
publish: true
---


::: tip
在这里总结`Python`使用技巧
:::

<!-- more -->

## `Cython` 基本用法
::::: tip Cython文件由两部分组成(和C类似)
- 定义： `.pxd`文件, 比如下面例子里的`cimport numpy as np`, 大致等于`#include <numpy/numpy.h>`
- 执行： `.pyx`文件

1. `ctypedef np.int_t DTYPE_t`: 之后便可以用 DTYPE_t 代替 np.int_t
2. `cdef numpy.ndarray arr`: 可以给所有参数以及返回值指定类型, 这里对 arr 进行强制类型定义
```python
ctypedef struct mycpx:
    float real
    float imag
cdef mycpx zz = {'real': 3.1415, 'imag': -1.0}
cdef mycpx zz = mycpx(real=2.718, imag=1.618034)
cdef mycpx zz = mycpx(3.1415, -1.0)
cdef numpy.ndarray[numpy.int_t, ndim=1] arr = numpy.arange(10, dtype=numpy.int)

cdef int my_min(int x, int y):
    return x if x <= y else y
```
::: right
循环尽量用`for-index`和`while`, 注意要把`n, m`设置为`C`可读的静态变量<br>
💥 pyx内部函数可以用`cdef`, 但如果希望函数被外部python调用, 要用`def`
:::
### 看看Cython有多快
:::: tabs type: card
::: tab main.py
这里用`Python`语法手动实现一个矩阵点乘的运算
```python
import numpy as np

def naive_dot(a, b):
    if a.shape[1] != b.shape[0]:
        raise ValueError('shape not matched')
    n, p, m = a.shape[0], a.shape[1], b.shape[1]
    c = np.zeros((n, m), dtype=np.float32)
    for i in range(n):
        for j in range(m):
            s = 0
            for k in range(p):
                s += a[i, k] * b[k, j]
            c[i, j] = s
    return c
```
:::
::: tab main_c.pyx
``` python
import numpy as np
cimport numpy as np
cimport cython

DTYPEf = np.float32         #numpy type alias
ctypedef np.float32_t DTYPEf_t

@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)   # turn off negative index wrapping for entire function
def naive_dot(np.ndarray[DTYPEf_t, ndim=2] a, np.ndarray[DTYPEf_t, ndim=2] b):
    if a.shape[1] != b.shape[0]:
        raise ValueError('shape not matched')
    cdef:
        int n = a.shape[0]
        int p = a.shape[1]
        int m = b.shape[1]
        np.ndarray[DTYPEf_t, ndim=2] c = np.zeros((n, m), dtype=DTYPEf)
        DTYPEf_t s
    c = np.zeros((n, m), dtype=DTYPEf)  #this is python
    for i in range(n):
        for j in range(m):
            s = 0
            for k in range(p):
                s += a[i, k] * b[k, j]
            c[i, j] = s
    return c
```
:::
::::
:::right
✨ 可以调用`cpython -a main_c.pyx`生成的`html`文件来分析哪些代码要与python互动
:::
:::::

- 我们现在可以通过编译`.pyx`, 得到可以被调用的`.pyd`文件, 和一个附带的`c`文件
    ```cmd
    python setup.py develop           #或者 python setup.py build_ext --inplace
    ```
    ::: details setup.py
    ```python 
    try:
        from setuptools import setup
        from setuptools import Extension
    except ImportError:
        from distutils.core import setup
        from distutils.extension import Extension

    from Cython.Distutils import build_ext
    import numpy

    ext_modules = [Extension(
        'main_c',                                #生成的库名称
        sources=['main_c.pyx'],                  #.pyx文件, 还可以加C文件
        include_dirs = [numpy.get_include()],    #gcc的-I参数
        # library_dirs=[],                       #gcc的-L参数
        # libraries=[],                          #gcc的-l参数
        # extra_compile_args=[],                 #比如 -std=C++11
    )]
                             
    setup(cmdclass = {'build_ext': build_ext}, ext_modules = ext_modules)
    ```
    :::

- __比较三段代码__: 计算100遍的运行时间, 重复3次实验, 取最小值; 可以看到在纯手工制造比`Cython`慢了近600多倍, 虽然数值优化过的`numpy`比`cython`还快(应该是空间换时间优化了算法)
    ```python{7,9,11}
    In [1]: import numpy as np
    In [2]: import dot_python
    In [3]: import dot_cython
    In [4]: a = np.random.randn(100, 200).astype(np.float32)
    In [5]: b = np.random.randn(200, 50).astype(np.float32)
    In [6]: %timeit -n 100 -r 3 main.naive_dot(a, b)
            675 ms ± 9.24 ms per loop (mean ± std. dev. of 3 runs, 100 loops each)
    In [7]: %timeit -n 100 -r 3 main_c.naive_dot(a, b)
            1.02 ms ± 72 µs per loop (mean ± std. dev. of 3 runs, 100 loops each)
    In [8]: %timeit -n 100 -r 3 np.dot(a, b)
            190 µs ± 62.6 µs per loop (mean ± std. dev. of 3 runs, 100 loops each)
    ```
### Cdef声明
<table>
    <thead>
        <tr>
            <th align="left">C变量类型</th>
            <th align="left">Cython指令</th>
            <th align="left">C变量类型</th>
            <th align="left">Cython指令</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">指针</td>
            <td align="left">cdef int *p<br>cdef void **buf</td>
            <td align="left">数组</td>
            <td align="left">cdef int [:] arr<br>cdef double points[20][30]</td>
        </tr>
        <tr>
            <td align="left">关联类型/别名</td>
            <td align="left">ctypedef size_t len</td>
            <td align="left">列表</td>
            <td align="left">cdef list particles</td>
        </tr>
        <tr>
            <td align="left">字典</td>
            <td align="left">cdef dict dictionary</td>
            <td align="left">字符串</td>
            <td align="left">cdef str pname</td>
        </tr>
        <tr>
            <td align="left">集合</td>
            <td align="left">cdef set unique_particles</td>
            <td align="left">无符号整型</td>
            <td align="left">unsigned int ind</td>
        </tr>
    </tbody>
</table>

::: right
也可以用函数修饰器`@cython.infer_types(True)`让cython对函数里的变量自动推断类型<br>
⏳ 目前可以自动推断的python类型包括: type, object, bool, tuple, date, time, timedelta, bytes, datetime
:::


## `Ipdb` 基本用法
::::: tip ipdb 调错
- 以前喜欢通过`log.info`来调错, 这里学习一下如何用`ipdb`这个工具来调错
- 在sublime中设置`tools->developer->new snippet`, 然后保存成`.sublime-snippet`文件
    ```python
    <snippet>
    <content><![CDATA[import ipdb; ipdb.set_trace()]]></content>
    <tabTrigger>pdb</tabTrigger>
    <scope>source.python</scope>
    <description>Insert a breakpoint</description>
    </snippet>
    ```

当设置了断点后, Python程序会在第一个断点之前停止运行, 常用Pdb命令包括
:::: tabs type: card
::: tab 基本
```{3-8}
h(elp)          帮助
q(quit)         退出
pp(rint)        漂亮打印
w(here)         当前位置
l(ist) 1,4      显示当前文件第1->4行 (ll打印整个文件)
a(rgs)          打印函数的参数
vars            列出对象的所有属性变量
dir/local       打印当前局部变量
```
:::
::: tab 移动
```{1}
<ENTER>         重复上一个操作, 相当于vim的.
n(ext)          执行下一条命令, 不进入函数内部运行过程
s(tep)          进入这一行的一个函数内部
u(p)            从step in函数中退出来
d(own)          又退进去?(move one level down in the stack trace)
r(eturn)        一直执行到函数的return
c(ontinue)      运行到下一个断点, 配合 b 使用
j(ump)          在同一个文件中跳跃(行)
```
:::
::: tab 断点
```{4}
b(reak)         显示当前所有断点和他们的ID
b(reak) 17      在当前文件第
b a/b:21        在当前路径下的`a/b.py`文件的第21行插入断点
b 17, i == 42   在local variable `i==42`的条件下加一个17行的断点
clear/disable/enable number      这个number就是断点的ID, 用`b`查询
```
:::
::::
:::::

!!!include(./python/sympy.md)!!!

## `Scipy` 基本用法

::::: tip scipy.stats, scipy.optimize
暂缺
:::: tabs type: card
::: tab 统计知识
- 包含随机变量分布, 估算函数, 和一些统计检验函数
- `beta.pdf(array, loc, scale)`地效果就是转换随机变量$Y=c+dX$, `cdf`同理, 注意我生成变量`beta.rvs()`的时候就是用的$\mu=5,\sigma=5$
```python
"""来自scipy.stats.beta"""
obs = beta.rvs(5, 5, size=2000)
grid = np.linspace(0.01, 0.99, 100)

fig, ax = plt.subplots()
ax.hist(obs, bins=40, density=True)
dist = beta.fit(obs); plt.title(r'$\mu = {:.2f}$'.format(beta.mean(*dist)))
ax.plot(grid, beta.pdf(grid, 5, 5), 'k-', linewidth=2, label='beta pdf')
ax.plot(grid, beta.cdf(grid, 5, 5), 'b:', linewidth=2, label='beta cdf')
```
![scipy-stats](~@assets/python_scipy_1.png#center)

- 除了用`fit`函数, 还有包括`linregress`这样的
```python
x = np.random.randn(200)
y = 2 * x + 0.1 * np.random.randn(200)
gradient, intercept, r_value, p_value, std_err = linregress(x, y)
gradient, intercept   # => (2.0004, -0.0075)
```
:::
::: tab 优化
比如我们现在要解
$$f(x) = \sin(4 (x - 1/4)) + x + x^{20} - 1, \quad x\in[0,1]$$
- 二分法：就是从$0~100$中间猜数字, 对半猜
- 牛顿-拉夫森：就是泰勒展开保留二次项的牛顿公式, $x = x_0 - f'(x_0)/f''(x_0)$, 但是这个方法好像只对单调函数有效, 比如这里凡是$x > 0.68$的都不会收敛到最优$ x^* = 0.41$
- 其他：牛顿法快，但鲁棒性弱，二分法稳定，但相对慢，有的方法是兼顾两者, 比如`brentq`
```python
"""二分 scipy.optimize.bisect"""
bisect(f, 0, 1) # => 0.40829
"""牛顿 scipy.optimize.newton"""
newton(f, 0.7)  # => 0.70017
"""其他 scipy.optimize.brentq"""
%timeit brentq(f, 0, 1)  
>> 26.2 µs ± 899 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
%timeit bisect(f, 0, 1)
>> 104 µs ± 1.28 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```
- 找最小值, 可以用`fminbound`, 多变量用`minimize`, `fmin`, `fmin_powell`, `fmin_cg`, `fmin_bfgs`, and `fmin_ncg`; 带限制条件的可以使用`fmin_l_bfgs_b`, `fmin_tnc`, `fmin_cobyla`
```python
"""求最大值 scipy.optimize.fminbound 但是这个答案也不对呀, 又掉局部最大去了"""
fminbound(lambda x: -f(x), 0, 1)  # => 0.70768
"""求最大值 scipy.optimize.minimize 这个稳, 而且method可以指定方法"""
minimize(lambda x: -f(x), (0.1,), bounds=((0,1),))['x'][0]  # => 1.0
```
![scipy-stats](~@assets/python_scipy_2.png#center)
:::
::::
:::::





## 参考

[1] [Cython 基本用法 @陈乐群](https://zhuanlan.zhihu.com/p/24311879)

[2] [Ipdb 调试大法 @PegasusWang](https://zhuanlan.zhihu.com/p/36810978)

[3] [SciPy 基本用法 @QuantEcon](https://python-programming.quantecon.org/scipy.html)