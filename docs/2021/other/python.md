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
::: tip Cython文件由两部分组成(和C类似)
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
:::
::: right
循环尽量用`for-index`和`while`, 注意要把`n, m`设置为`C`可读的静态变量<br>
💥 pyx内部函数可以用`cdef`, 但如果希望函数被外部python调用, 要用`def`
:::
### 看看Cython有多快
:::: tabs
::: tab main.py
这里用`Python`语法手动实现一个矩阵点乘的运算
```python
import numpy as np

def naive_dot(a, b):
    if a.shape[1] != b.shape[0]:
        raise ValueError('shape not matched')
    n, p, m = a.shape[0], a.shape[1], b.shape[1]
    c = np.zeros((n, m), dtype=np.float32)
    for i in xrange(n):
        for j in xrange(m):
            s = 0
            for k in xrange(p):
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

我们现在可以通过编译`.pyx`, 得到可以被调用的`.pyd`文件, 和一个附带的`c`文件
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

__比较三段代码__: 计算100遍的运行时间, 重复3次实验, 取最小值; 可以看到在纯手工制造比`Cython`慢了近600多倍, 虽然数值优化过的`numpy`比`cython`还快(应该是空间换时间优化了算法)
```python{7,9,11}
In [1]: import numpy as np
In [2]: import dot_python
In [3]: import dot_cython
In [4]: a = np.random.randn(100, 200).astype(np.float32)
In [5]: b = np.random.randn(200, 50).astype(np.float32)
In [6]:  %timeit -n 100 -r 3 main.naive_dot(a, b)
        675 ms ± 9.24 ms per loop (mean ± std. dev. of 3 runs, 100 loops each)
In [7]:  %timeit -n 100 -r 3 main_c.naive_dot(a, b)
        1.02 ms ± 72 µs per loop (mean ± std. dev. of 3 runs, 100 loops each)
In [8]:  %timeit -n 100 -r 3 np.dot(a, b)
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



## 参考

[1] [Cython 基本用法 @陈乐群](https://zhuanlan.zhihu.com/p/24311879)