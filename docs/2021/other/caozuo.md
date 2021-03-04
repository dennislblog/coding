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

## 批量转换Jupyter
```
workon imitate & jupyter nbconvert --to html *.ipynb
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

##IPython指令
```python
%precision 4        # sets printed precision for floats to 4 decimal places
%whos               # gives a list of variables and their values
%quickref           # gives a list of magics
```