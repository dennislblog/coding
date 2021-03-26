---
title: 计算机命令
date: 2021-01-31
autoGroup-3: 知识 
categories:
    - Knowledge
tags:
    - Tool
sidebarDepth: 3
publish: true
---

::: tip
在这里记录计算机批处理小技巧 (win + L to locker the computer)
:::

<!-- more -->

## Latex相关
```tex
% 1. inline mode 数学公式超出边界, 做法就是在document加\sloppy
\begin{document}\sloppy
...
\end{document}

% 2. conditonal on 符号, 用bigg或者更大的Bigg, 然后rvert是丨, 如果是希望自动调整高度
\left. \frac{1}{H(\hat S)} \right\rvert_{y=Y}

% 3. 在align环境下如果想把label放在某一行, 得每行后面加\nonumber

```

## Git相关
参考资料： [subtree教程](https://segmentfault.com/a/1190000012002151)
```
1. 创建远程分支
git remote add deploy https://github.com/dennislblog/infosys.git

2. 以某一个文件夹为蓝本在当前目录下创建一个子分支child, squash表示不考虑过往commit
git subtree split --prefix=other --squash --branch child

3. 清除远程与本地不兼容的文件
git rm -r --cached to-delete-folder
git add . => git commit -m "msg" => git push remote local

4. 突然告诉我Connection was reset in connection to github.com:443
#  从电脑-settings-proxy找到代理端口, 我现在的VPN是10809, 之后reset就好了
git config --global http.proxy 127.0.0.1:10809
git config --global https.proxy 127.0.0.1:10809
```

## 自动生成安装依赖
加"encoding"是考虑有汉字注释的原因
```
pipreqs --encoding=utf-8 ./
```

## Python对象占用内存大小
```python
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

"""返回比特字节
get_size(instance)
>> 3.037754 x 1e6 bytes
"""
```

## 子文件夹
Move all files from subdirectories to current directory
```
mv */*.ipynb .                     #将子文件夹内ipynb文件全部放到当前文件夹
find . -type d -empty -delete      #将内容为空的子文件夹删除
```

## 批量转换Jupyter
```
workon imitate & jupyter nbconvert --to html *.ipynb

# pip 换源
pip config set global.index-url http://pypi.python.org/simple/
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

# conda 换源 (.condarc文件)
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes  #显示包的来源
conda config --remove-key channels        #清空源配置, 出国
```

## 在错误出现之前调错
```
python -m ipdb -c continue *.py
```

## Python画图全局尺寸
```python
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 10, 3
```
## Python改变小数精度
```python
np.set_printoptions(precision = 4)
# 或者直接 %precision 4
```
## Python处理遍历失败
```python
"""在for循环完整完成后才执行else, 如果中途跳出循环, 则一并跳过else语句
"""
for i in range(n):
    if f(i) >= threshold: break
else:
    print("all below threshold")
```

## Jupyter自动补全
Jupyter lab中的TAB键失去作用, [参考这里](https://stackoverflow.com/questions/44186370/kernel-taking-too-long-to-autocomplete-tab-in-jupyter-notebook)
```python
# 进入ipython_config.py
c.Completer.use_jedi = False
```

## Jupyter-Plotly一片空白
折腾半天，发现Windows上安装还是傻逼安装最[简单](https://nodejs.org/en/download/)
```python
# 安装 nodejs
conda install -c conda-forge nodejs  
# 安装jupyer lab plotly
jupyter lab clean; jupyter lab build
```
但是他给我报错, 好像是[webpack](https://github.com/jupyterlab/jupyterlab/issues/9533)的问题, 于是更新jupyterlab到`3.0.6`
```python
# 更新jupyter lab
pip install --upgrade jupyterlab
jupyter labextension install jupyterlab-plotly
# 现在可以运行plotly了
import plotly.express as px
fig = px.line(x=["a","b","c"], y=[1,3,2], title="sample figure")
fig.show()
```

## IPython指令
```python
%precision 4        # sets printed precision for floats to 4 decimal places
%whos               # gives a list of variables and their values
%quickref           # gives a list of magics
```

## NPM安装错误
直接`npm install --ignore-scripts`
```python
"""
gyp ERR! stack     import sys; print "%s.%s.%s" % sys.version_info[:3];
"""
```

## 更新环境变量
```
set PATH=C #关闭后再打开 echo %PATH% 可以看见更新的路径
```

## 关闭占用端口程序
这里示范怎么把占用端口$8891$的程序后台强行关闭
```
netstat -ano | findstr 8891
# TCP    127.0.0.1:8891         0.0.0.0:0              LISTENING       40128
taskkill /F /PID 40128
# SUCCESS: The process with PID 40128 has been terminated.
```