---
title: DolphinDB介绍
date: 2021-01-08
autoGroup-2: 工具
categories:
  - Tutorial
tags:
  - Tool
sidebarDepth: 2
publish: true
---

::: tip
在这里记录数据获取和处理
:::

## 数据库

![总体架构](~@assets/dolphin-03.png#center)

### 启动服务器

Python应用通过会话（Session）在DolphinDB服务器上执行脚本和函数以及在两者之间双向传递数据。常用的Session类的函数如下：

<table>
    <thead>
        <tr>
            <th align="left">方法名</th>
            <th align="left">详情</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">connect(host,port,[username,password])</td>
            <td align="left">将会话连接到DolphinDB服务器</td>
        </tr>
        <tr>
            <td align="left">login(username,password,[enableEncryption])</td>
            <td align="left">登录服务器</td>
        </tr>
        <tr>
            <td align="left">run(DolphinDBScript)</td>
            <td align="left">将脚本在DolphinDB服务器运行</td>
        </tr>
        <tr>
            <td align="left">run(DolphinDBFunctionName,args)</td>
            <td align="left">调用DolphinDB服务器上的函数</td>
        </tr>
        <tr>
            <td align="left">upload(DictionaryOfPythonObjects)</td>
            <td align="left">将本地数据对象上传到DolphinDB服务器</td>
        </tr>
        <tr>
            <td align="left">undef(objName,objType)</td>
            <td align="left">取消指定对象在DolphinDB内存中定义以释放内存</td>
        </tr>
        <tr>
            <td align="left">undefAll()</td>
            <td align="left">取消所有对象在DolphinDB内存中的定义以释放内存</td>
        </tr>
        <tr>
            <td align="left">close()</td>
            <td align="left">关闭当前会话</td>
        </tr>
    </tbody>
</table>

在`dolphindb.cfg`中可以修改默认端口号(暂时是8900), 如果需要指定其它端口，可以执行
```
start server/dolphindb.exe -localSite localhost:post:name
```
对`https`进行通讯加密
```
s=ddb.session(enableSSL=True)
```

### 导入数据到服务器

:fist:
用`loadText`方法把文本文件导入到DolphinDB的**内存表**中，注意`DATA_DIR`必须是完整路径, 而且注意`windows`操作系统下奇怪的路径。 默认分割符是逗号
```python
DATA_DIR =r'C://Users//denni//thesis_2021//thesis_impact//tools//_dolphindb_//data'
trade = s.loadText(DATA_DIR+'//example.csv', delimiter=',')
```
:fist_right:
如果数据太大，超过内存读取要求，可以创建分区数据表(可以是DFS也可以是内存表), 由于一旦创建了数据库，就不能更改他的`partition scheme`，因此得先确定这个数据库是否已经存在于服务器了

```python
if s.existsDatabase(WORK_DIR+"/valuedb"):
    s.dropDatabase(WORK_DIR+"/valuedb")
```
::: right
若是值分区或范围分区 (value/range)，可以通过addValuePartitions和addRangePartitions来添加分区
:::
:ok_hand:
这里我们简单地使用股票名称分割, 还可以使用范围/列表/组合分区，详细看[这里](https://www.dolphindb.cn/cn/help/database1.html)
```python
# 1 硬盘存取 
s.database(dbName='db', partitionType=ddb.VALUE, partitions=["AMZN","NFLX","NVDA"], dbPath=WORK_DIR+"/valuedb")
# 2 distributed file system
s.database(dbName='db', partitionType=ddb.VALUE, partitions=["AMZN","NFLX", "NVDA"], dbPath="dfs://valuedb")
```
:point_right:
创建数据库后，按照`partition scheme`载入数据(用`loadTextEx`函数), 如果分割表不存在就创建一个，如果存在就`append`
- loadText方法把文本文件导入到DolphinDB的内存表中
- ploadText方法可以并行加载文本文件到内存分区表中，比loadText要快
- loadTextEx把数据导入到分区内存表中(有`partition`的)
```python
filePath=WORK_DIR + "/example.csv"
trade = s.loadText(filePath)
trade = s.loadTextEx(dbPath="db", tableName='trade', partitionColumns=["TICKER"], remoteFilePath=filePath)
trade = s.ploadText(filePath))
```

### 从服务器加载数据

调用`loadTable(tableName, dbPath)`读取和查看服务器端的表格，如果没有指定`dbPath`会试图从内存中加载表格。 下图是分区表中一个特定分区`AMZN`的结构(每一个都是一张内存表)。 数据以列的形式被存储起来
```
├───AMZN
│   │   trade.tbl
│   │
│   └───trade
│           ASK.col
│           BID.col
│           date.col
│           PRC.col
│           TICKER.col
│           VOL.col
```
`loadTable`可以让我们只读取分区的数据
```python
# 1. pload 比 loadtext 要更快
trade=s.ploadText(WORK_DIR+"/example.csv")
# 2. 可以按照分割标准只加载一部分
trade = s.loadTable(tableName="trade",dbPath=WORK_DIR+"/valuedb", partitions="AMZN")
# 3. 还可以用SQL语句加载
trade = s.loadTableBySQL(tableName="trade", dbPath=WORK_DIR+"/valuedb", sql="select * from trade where date>2010.01.01")
```
::: details Dolphindb -> Python 数据转换
![数据转换](~@assets/dolphin-01.png#center)
> __此外还有几种数据结构的映射__
>  
![数据结构](~@assets/dolphin-02.png#center)
:::

### 上传服务器

:one: 
使用`session.upload`可以上传一个Python的字典对象，它的key对应的是DolphinDB中的变量名，value对应的是Python对象，可为Numbers，Strings，Lists，DataFrame等数据对象。
```python
df = pd.DataFrame({'id': np.int32([1, 2, 3, 4, 3]), 
	'value':  np.double([7.8, 4.6, 5.1, 9.6, 0.1]), 'x': np.int32([5, 4, 3, 2, 1])})
s.upload({'t1': df})
print(s.run("typestr(t1)"))
```
:two: 
也可以直接创建`DolphinDB table object`, 这里`executeAs`可以给表重命名(也可以用`tableAliasName='test'`作为参数传入`session.table`)
::: details 为什么要重命名
Python端通过session.table函数将数据上传到server之后，DolphinDB会建立一个Python端变量对server端table变量的引用。 但是在给Python端`dt`分配服务器的`test`表之前，要确保`test`表没有引用其他Python本地对象, 否则要么释放`test`, 要么创建另外一个服务器表。 

最合理的做法是在创建`session.table`的时候不指明表的名称, 这样会为用户随机产生一个临时表名(通过`t.tableName()`获取)。 但这样会不会导致服务器端产生大量无用表，造成内存溢出呢？ 只要我们在本地Python端用的是同一个变量名，当更新引用的时候，之前引用这个对象的表自动被释放。 
:::
```python
# table(capacity:size, colNames, colTypes)
dt = s.table(data={'id': [1, 2, 2, 3], 'ticker': ['AAPL', 'AMZN', 'AMZN', 'A'],
                   'price': [22, 3.5, 21, 26]}).executeAs("test")
print(s.loadTable("test").cols == dt.cols)
```
:three: 
然后我们可以对`dolphindb.table.Table`对象进行操作, 包括append, update, where, delete, drop等
```python
t = trade.top(2).executeAs("top2")
trade = trade.append(t)
trade.where('ticker=`AMZN && BID==ASK && date>=2010.01.01').toDataFrame()
s.run('tableInsert{}')
"""
  TICKER       date  ...        BID        ASK
0   AMZN 2010-04-29  ...  141.78999  141.78999
1   AMZN 2010-11-08  ...  172.07001  172.07001
"""
trade = trade.update(["VOL"],["999999"]).where("TICKER=`AMZN")
trade.delete().where('date<2013.01.01').execute()
tarde=trade.drop(['ask', 'bid'])
```

## API

::: details 会话
- nullValueToZero: 
- nullValueToNan:
- subscribe/unsubscribe
- getInitScript/setInitScript
- saveTable/loadTable/loadTableBySQL/loadTextEx
- loadText/ploadText
- convertDatetime64
- existsDatabase/dropDatabase
- dropPartition
- existsTable/dropTable
- undef/undefAll
- clearAllCache
- table
:::

::: details 数据库
- createTable
- createPartitionedTable 
:::

::: details 数据表
- select(cols)
- where(conds)
- groupby/contextby/pivotby(cols): 下例展示了group by和context by的[不同之处](http://www.dolphindb.cn/cn/help/index.html?getAllDBs.html)
- top/sort/rows/cols/schema
- execute(expr)
- merge/merge_asof/merge_window/merge_cross
- showSQL: 翻译成SQL <br>`select {top} {select} from {table} {where} {groupby} {having} {orderby}`
- append(table)/update(cols,vals)/delete/drop(cols)
- rename(name)/executeAs(name)
- ols(Y,X,intercept=True)
- toDF
:::


## 应用情境

### 获取数据库中的所有表

```python
db = s.database(dbName='mydb', dbPath=DATA_DIR+'//thesisdb')
print(s.run('getTables(mydb)'))
>> ['trade']
```

### 数据表的输入和输出
```python
trade = s.table(data=createDemoDF(), tableAliasName="tradeData")
s.saveTable(tbl=trade, dbPath=DATA_DIR+'//testdb')
s.loadTable(tableName='tradeData',  dbPath=None, partitions=None, memoryMode=False)
# database, loadTable 和 loadTableBySQL 三步操作
trade = s.loadTableBySQL(tableName="trade", dbPath=WORK_DIR+"/valuedb", 
	sql="select * from trade where date>2010.01.01") 
```
::: right
注意这里的`dbPath`必须是没有被分配的地址, 因为要创建一个非分区数据库。 <br>
另外也可以用`loadTableBySQL`更灵活, 但那样返回的只能是内存分区表, 而且比较费时
:::




## 参考资料

- [Python API for DolphinDB @dolphindb](https://github.com/dolphindb/api_python3/tree/master)