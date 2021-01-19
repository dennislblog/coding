---
title: 回测框架
date: 2021-01-19
autoGroup-2: 工具 
categories:
    - Knowledge
tags:
    - Tool
sidebarDepth: 3
publish: true
keys: 
    - 'e256df09eb48f2ef04fc6c88a44b1b61'
---

::: tip
本文基于[bt @pmorissette](https://github.com/pmorissette/bt/tree/dev), 理解原理和进行一点魔改
:::

<!-- more -->

## 获取数据

由`ffn`的`get`接口提供
:::: tabs type: card
::: tab 参数
* tickers (list, string, csv string): 例如 `'msft,c,gs,ge'`
* provider (function): 接口函数, 默认是雅虎引擎, 我想把数据库接口写进去(参考那个csv)
* common_dates (bool): 只保留所有ticker都有数据的日期
* forward_fill (bool): 当`common_dates=False`, 这个设定会用第一个非NA填充缺失
* clean_tickers (bool): 处理列标签
    ```python
    clean_ticker('^VIX'); clean_ticker('SPX Index')
    >> 'vix'; 'spx'
    ```
* column_names (list): 指定列标签
* ticker_field_sep (char): 只下载部分数据, 例如 AAPL:Low 只下载AAPL的low那一列
* mrefresh (bool): 不留缓存
* existing (DataFrame): 把下载的数据append到已有数据, 这里数据库接口也要处理一下
* kwargs: 例如`start='2010-01-01'`

然后我们得到一个 `time x tickers` 的dataframe
```
            c           gs          ge
Date            
2009-12-31  29.361824   143.514740  10.605983
2010-01-04  30.160183   147.118881  10.830304
2010-01-05  31.313356   149.719818  10.886385
```
:::
::: tab to do
- 把数据库接口写进去
:::
::::

## 写策略

由`bt`的`Strategy`接口提供

:::: tabs type: card
::: tab 参数
* name (str): 策略名称
* algos (list): 对获取数据的一系列处理, 无法并行, 只要其中一条算法返回False, 策略停止
* children (dict, list): 如果需要创建策略的子策略
* now (datetime): 遍历获取数据使用的指针, 例如`Timestamp('2021-01-15 00:00:00')`
* prices (TimeSeries): Security prices. ?? `self.price`指向最近价格
* full_name (str): Name including parents' names
* members (list): Current Security + strategy's children
    ```python
    sma10.strategy.members
    # 每一个都是一个策略
    >> [<Strategy sma10>, <SecurityBase sma10>ge>, <SecurityBase sma10>c>, <SecurityBase sma10>gs>]
    ```
:::
::: tab 结果
* name: sma10
* parent = root = `<Strategy sma10>`
* children: `{'ge': Str>ge>, 'c': Str>c>, 'gs': Str>gs> }`
* now: 2021-01-15 00:00:00
* commission_fn: ??
* bankrupt: True if capital < 0
* temp: {'selected': ['gs', 'ge'], 'weights': {'gs': 0.5, 'ge': 0.5}} 临时存储的数据, 每一次run都会清除
* perm (dict): Permanent data used to pass info from one algo to another. Not cleared on each pass.
* data: 统计策略效益 ??为啥多个资产, 就一个价格?
    ```python
                     price         value        cash  fees
    2021-01-13  235.157729  2.351577e+06  215.803660   0.0
    2021-01-14  239.563307  2.395633e+06  276.344126   0.0
    2021-01-15  229.993571  2.299936e+06  116.473505   0.0
    ```
* positions: 
    ```python
                     ge       c     gs
    2021-01-13  67749.0 11723.0 2587.0
    2021-01-14  68485.0 11571.0 2593.0
    2021-01-15  101497.0    0.0 3820.0
    ```
:::
::: tab to do
* 把强化学习策略写进去
:::
::::

## 做回测

由`bt`的`Backtest`接口提供, 这个是策略的返回对象, 参数主要是单一策略和对象数据

:::: tabs type: card
::: tab 参数
* initial_capital (float): 起始资金(不破产), 默认1000000
* commissions (fn(quantity, price)): 中介费, 例如 `commissions=lambda q, p: max(1, abs(q) * 0.01)`
* progress_bar (Bool): 是否显示运行进度
<br>属性
* weights: 策略下不同资产的持有净值(不是position, 是value)
    ```
              sma10   sma10>ge     sma10>c    sma10>gs
    2021-01-13  1.0   0.333332    0.333308    0.333268
    2021-01-14  1.0   0.333329    0.333321    0.333234
    2021-01-15  1.0   0.499997    0.000000    0.499952
    ```
* positions: 不同资产的position
    ```
                      ge      c     gs
    2021-01-13  67749.0 11723.0 2587.0
    2021-01-14  68485.0 11571.0 2593.0
    2021-01-15  101497.0    0.0 3820.0
    ```
* security weights: 
    ```
                      ge           c          gs
    2021-01-13  0.333332    0.333308    0.333268
    2021-01-14  0.333329    0.333321    0.333234
    2021-01-15  0.499997    0.000000    0.499952
    ```
* herfindahl_index: HHI is defined as a sum of squared weights of securities in a portfolio `(weights ** 2).sum(axis=1)`
* turnover: Turnover is defined as the lesser of positive or negative outlays divided by strategy.values
:::
::: tab 结果

:::
::::