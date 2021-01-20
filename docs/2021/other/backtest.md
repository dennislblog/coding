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

![回测结果](~@assets/bt-01.png#center)

## 获取数据

由`ffn`的`get`接口提供
:::: tabs type: card
把数据库接口写进去
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
```python
            c           gs          ge
Date            
2009-12-31  29.361824   143.514740  10.605983
2010-01-04  30.160183   147.118881  10.830304
2010-01-05  31.313356   149.719818  10.886385
```
:::
::: tab 补充
- 补充
:::
::::

## 写策略

由`bt`的`Strategy`接口提供

:::::: tabs type: card
想办法把强化学习策略写进去
::::: tab 组件
:::: tabs type: card
```python
s = StrategyBase('s')
>> data
                 c1  c2
    2010-01-01  100 200
    2010-01-02  300 100
    2010-01-03  150 50
s.setup(data); s.update(dts[0])         #now that we have c1/c2 price at 01.01
s.adjust(300)                           #inject 300 to s
s.allocate(250, 'c1'); c1 = s['c1']     #use 250 to buy c1
```
::: tab adjust
注入资金, 但对子账户无效
```python
c1 = SecurityBase('c1')
c2 = SecurityBase('c2')
s = StrategyBase('p', [c1, c2])
s.adjust(1000)
>> s.capital == s.value == 1000
>> c1.value == c1.weight == 0
```
:::
::: tab close
关户: 当资产价格为0或者不存在某个资产, 账户仓位清空
```python
>> c1.position == 2.0
>> s.capital == -200.0             #但是如果s['c1']里allocate money就不用从s里扣了
s.close('c1')                      #以`c1`当前价格清仓
>> c1.position == 0
>> s.capital == 0
```
:::
::: tab flatten
把所有子账户清仓
```python
s.adjust(300); s.allocate(200, 'c1')
>> s.value == 300; s.capital == 100
>> c1.position = 2; c1.value == 200
s.flatten()
>> c1.value == c1.position == 0
>> s.capital == s.value == 300
```
:::
::::
:::::
::::: tab 参数
* name: sma10 - 策略名称
* algos (list): 对获取数据的一系列处理, 无法并行, 只要其中一条算法返回False, 策略停止
* parent = root = `<Strategy sma10>`
* children(dict, list): 假设资产组合为`ibm, tsla, msft`, 那么策略就会有
    ```python
    S.children
    >> {'ibm': <SecurityBase sma10>ibm>, 'tsla': <SecurityBase sma10>tsla>, 'msft': <SecurityBase sma10>msft>}
    ```
* now (datetime): 遍历获取数据使用的指针, 例如`Timestamp('2021-01-15 00:00:00')`
* prices (TimeSeries): Security prices. ?? `self.price`指向最近价格
* use_integer_positions (bool): 是否要求所有资产的持仓位必须是整数, 默认是, 但可以考虑fractional trading
* temp: {'selected': ['gs', 'ge'], 'weights': {'gs': 0.5, 'ge': 0.5}} 临时存储
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
:::::
::::: tab 评估
基于`ffn.core.PerformanceStats`接口
* prices(series): 从start-date到end-date每天一个
* rf(float or series): risk-free rate, 可以设置也可以是一个pd.series
* float: daily_mean, daily_vol, daily,sharpe, daily_sortino, cagr(compound annual growth rate)
* float: best_day, worst_day: 回报的最大/最小值; total_return: 总回报
* drawdown (series): 从最近历史最高点价格往下的幅度, `drawdown_details`刻画的更仔细
* float: daily_skew, daily_kurt
* series: monthly_returns, yearly_returns
* return_table: 显示每年每个月的回报率
    ```python
            Jan         Feb         Mar         Apr         May         Jun         Jul         Aug         Sep         Oct         Nov         Dec         YTD
    2009    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000
    2010    -0.040719   -0.014114   0.138134    -0.063934   -0.039809   -0.141698   0.056001    -0.025762   0.002530    0.050998    -0.000068   0.119172    0.007318
    2011    -0.007785   -0.002383   -0.042651   0.006071    -0.027695   0.022592    -0.039414   -0.036690   -0.171185   0.155409    -0.152653   0.083666    -0.228694
    2012    0.117055    0.026763    0.025129    -0.085272   -0.031195   0.061719    -0.007211   0.050128    0.125111    0.040017    -0.030030   0.023678    0.340039
    2013    0.094995    0.001551    0.007742    0.010723    0.083662    -0.088852   0.062815    -0.023802   0.036344    0.012230    0.057299    0.011057    0.283221
    ```
:::::
::::: tab 算法
`AlgoStack(*algos)(self)` >> 前者是在回测建立时, 依序放进栈里的算法，后者是策略本身
```python
self.stack.algos
>> (<bt.algos.SelectWhere object at 0x0000020527B32310>, <bt.algos.WeighEqually object at 0x0000020527B32400>, <bt.algos.Rebalance object at 0x0000020527B32A30>)
```
:::: tabs type: card
::: tab SelectWhere
`signal`是算法创建时根据数据得到的信号(true/false)
```python{5}
             ibm  tsla   msft
Date
2021-01-14  True  True  False
2021-01-15  True  True  False
2021-01-19  True  True   True
```
:::
::: tab WeighEqually
对上一步中被选中的股票进行权重分配
```python
target.temp['selected']
>> ['tsla', 'msft']
target.temp['weights']
>> {'tsla': 0.5, 'msft': 0.5}
```
:::
::::
:::::
::::::

## 做回测

由`bt`的`Backtest`接口提供, 这个是策略的返回对象, 参数主要是单一策略和对象数据

:::::: tabs type: card
::::: tab 参数
* initial_capital (float): 起始资金(不破产), 默认1000000
* commissions (fn(quantity, price)): 中介费, 例如 `commissions=lambda q, p: max(1, abs(q) * 0.01)`
* progress_bar (Bool): 是否显示运行进度
<br>属性
* weights: 策略下不同资产的持有净值(不是position, 是value)
    ```python
              sma10   sma10>ge     sma10>c    sma10>gs
    2021-01-13  1.0   0.333332    0.333308    0.333268
    2021-01-14  1.0   0.333329    0.333321    0.333234
    2021-01-15  1.0   0.499997    0.000000    0.499952
    ```
* positions: 不同资产的position
    ```python
                      ge      c     gs
    2021-01-13  67749.0 11723.0 2587.0
    2021-01-14  68485.0 11571.0 2593.0
    2021-01-15  101497.0    0.0 3820.0
    ```
* security weights: 
    ```python
                      ge           c          gs
    2021-01-13  0.333332    0.333308    0.333268
    2021-01-14  0.333329    0.333321    0.333234
    2021-01-15  0.499997    0.000000    0.499952
    ```
* herfindahl_index: HHI is defined as a sum of squared weights of securities in a portfolio `(weights ** 2).sum(axis=1)`
* turnover: Turnover is defined as the lesser of positive or negative outlays divided by strategy.values
:::::
::::: tab 步骤
1. 确定策略和数据的映射
    ```python
    # 例如 long_only_ew 策略
    def long_only_ew(tickers, start='2019-01-01', name='long_only_ew'):
        s = bt.Strategy(name, [bt.algos.RunOnce(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
        data = bt.get(tickers, start=start)
        return bt.Backtest(s, data)
    ```
2. 执行策略
:::: tabs type: card
::: tab backtest.run
```python
def run(self):
    if self.has_run:
        return
    self.has_run = True
    self.strategy.setup(self.data)
    self.strategy.adjust(self.initial_capital)
    self.strategy.update(self.dates[0])
    for dt in self.dates[1:]:
        self.strategy.update(dt)
        if not self.strategy.bankrupt:
            self.strategy.run()
            self.strategy.update(dt)
    self.stats = self.strategy.prices.calc_perf_stats()
```
:::
::: tab strategy.setup
```python
def setup(self, universe):
    self._prices = prices = universe[self.name]
    self.data = pd.DataFrame(index=universe.index,
                                 columns=['value', 'position'],
                                 data=0.0)
    self._prices_set = True
    self._values = self.data['value']
    self._positions = self.data['position']
```
- cash, fees, funiverse, prices
:::
::: tab strategy.adjust
```python
def adjust(self, amount, update=True, flow=True, fee=0.0):
    self._capital += amount
    self._last_fee += fee
    if flow: self._net_flows += amount #example includes a capital injection every month
    if update: self.root.stale = True  #indicate data is now stale and need update before access
```
- stale, net_flow and capital
:::
::: tab strategy.update
```python
def update(self, date, data=None, inow=None):
    self.root.stale = False  #now we upate the stale data to enable its access
    """
    1. update data if now.value changed, or now is different than date
    2. update all children data if parent needs to update
    3. 
    """
```
- on date/inow index: update price, cash, value and all udpates can be seen on `strategy.data`, stale now goes back to False (meaning already updated) and update now to be current timestamp (i.e., date). 
:::
::: tab strategy.run
```python
def run(self):
    self.temp = {}     #clear out tmp data
    self.stack(self)   #run algo stack
    for c in self._childrenv:
        c.run()        #run children 
```
:::
::::
:::::
::::::


