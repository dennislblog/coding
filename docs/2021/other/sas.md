---
title: SAS技巧
date: 2021-04-07
autoGroup-3: 知识 
categories:
  - Knowledge
tags:
  - Risk
sidebarDepth: 3
publish: true
---


::: tip
这里记录SAS语言学习
:::

<!-- more -->


## 基本操作

::: tip
🍖 将文件按照某一列分解为若干个CSV
```sas
/* 下面这个代码将have数据表按照source分成三个文件trade_A.csv, trade_B.csv, trade_C.csv*/
data have;
infile cards;
input hatch source $ Value $;
cards;
1   A   this
2   A   that
1   B   here
2   C   there
;
proc sql noprint;
select distinct source into:sources separated by ' ' from have;
quit;

%macro splitData(key=, basename=);
%do i=1 %to %sysfunc(countw(&key));
    %let src=%scan(&key,&i);
    data &basename&src;
        set have;
        where source="&src";
    run;
    %let obs=;
    data _null_;
        if _n_=1 then
        set  &basename&src nobs=nobs;
        call symputx('obs',nobs);
    run;
    %if &obs>0 %then %do;
        proc export outfile="&basename&src..csv" dbms=dbf replace;
    run;
%end;
%mend;
%splitData(sources=&sources, basename=trade_)
```
:::

::: tip
![](~@assets/sas_basic-01.png#small)
🥔 有一个数据集`have`, 有三个变量`A,B,C`, 想新建一个变量`D`添加到`B`和`C`中间, 怎么做
```sas
proc sql ;
    select name into :names separated by ","
    from dictionary.columns
    where libname="SASHELP" and memname="CLASS";
quit;
%put &names;    /* Name,Sex,Age,Height,Weight */

data test;
    vars="&names";
    vars_new=tranwrd(vars,"Sex","'something' as New_Var");
    call symput("new_names",vars_new);
run;
%put &new_names;    /* Name,Sex,'something' as New_Var,Age,Height,Weight */

proc sql;
    create table test as
    select &new_names
    from sashelp.class;
quit;
```
:::


::: warning
🥕 打印数据表的所有列名称
```sas
/* you may load the data into WORK lib already */
proc sql noprint;
  select name into :names separated by ","
  from dictionary.columns
  where libname="TMP1" and memname=upcase("name_of_the_data")
  ;
quit ;
%put &names;  
```
:::

::: warning
🍌 写了我两个小时, 代码竟这么短😭 如何将一个大文件按照日期和股票标识进行拆分
- 在他的服务器上只跑了20分钟, 哎, 差距呀, 如果也能跑机器学习就好了(限制了深度学习框架)
- SAS可以写深度学习吗? 🤪
```sas
/* 
qsas  - 提交任务, 貌似只能在云里操作
qstat - 查看任务状态
qdel  - 从队列里删除任务 
*/
proc sql noprint;
  select distinct date into:dates separated by ' ' from LARGEFILE;
  select distinct sym_root into:tickers separated by ' ' from LARGEFILE;
quit;

%macro splitData(dates=, tickers=, basename=);
%do i=1 %to %sysfunc(countw(&dates));
  %do j=1 %to %sysfunc(countw(&tickers));
      %let date=%scan(&dates,&i); %let ticker=%scan(&tickers,&j);
      data &basename&ticker&date;
          set LARGEFILE;
          where date="&date"d and sym_root="&ticker";
      run;
      %let obs=;
      data _null_;
          if _n_=1 then
          set  &basename&ticker&date nobs=nobs;
          call symputx('obs',nobs); 
      run;
      %if &obs>0 %then %do;
      %let date_new=%sysfunc(inputn(&date, date9.), yymmddn8.);
          proc export outfile="/scratch/udel/dennislx/output/&basename._&ticker._&date_new..csv" dbms=csv label replace;
      run;
    %end;
  %end;
%end;
%mend;
%splitData(dates=&dates, tickers=&tickers, basename=profile)
```
:::