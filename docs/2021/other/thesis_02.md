---
title: 数据
date: 2020-01-07
autoGroup-2: 论文
categories:
  - Paper
tags:
  - Thesis
publish: false
sidebarDepth: 2
---

::: tip
在这里记录数据获取和处理
:::

## 数据库

__启动服务器__

在`dolphindb.cfg`中可以修改默认端口号(暂时是8900), 如果需要指定其它端口，可以执行
```
start server/dolphindb.exe -localSite localhost:post:name
```

__加载数据__

`DATA_DIR`输入完整路径, 而且注意`windows`操作系统下奇怪的路径
```
s = ddb.session()
s.connect("localhost",9031,"admin","123456")
trade = s.loadText(DATA_DIR)

  TICKER       date      VOL    PRC   BID     ASK
0   AMZN 1997-05-15  6029815  23.50  23.5  23.625
1   AMZN 1997-05-16  1232226  20.75  20.5  21.000
2   AMZN 1997-05-19   512070  20.50  20.5  20.625
```
