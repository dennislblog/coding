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
在这里记录计算机批处理小技巧
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