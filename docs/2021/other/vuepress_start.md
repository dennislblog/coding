---
title: 用Vuepress搭建博客
date: 2020-01-01
autoGroup-2: 工具
categories:
  - Tutorial
tags:
  - VuePress
---

::: tip
本来gitbook用的挺好的，有些需要定制的功能找到到API，所以转向了开放度更高的Vue. 利用这篇博客学习搭建`Vuepress`的技术
:::

<!-- more -->


## 支持Tex语法

$$\begin{aligned}
  a&=b+c \cr
  d+e&=f \\[1em]
     &=\Big( r(s,a) + \gamma V^*(s') \Big)
\end{aligned}$$

## 支持MultiTabs操作

:::: tabs
::: tab python
```python
print("Python code example")
```
:::
::: tab javascript
``` javascript
() => {
  console.log('Javscript code example')
}
```
:::
::: tab java
``` javascript
public static void main(String args[]){  
 System.out.println("Hello Java");  
}  
```
:::
::::

## Emoji
参考[这里](https://emoji.muan.co/), 就是显示有点奇怪, 可能是我没有安装特定字体的缘故

## 容器
默认有`tip`,`warning`,`danger`,`theorem`,`right`和`details`
::: theorem 牛顿第一定律
假若施加于某物体的外力为零，则该物体的运动速度不变。

::: right
来自 [维基百科](https://zh.wikipedia.org/wiki/%E7%89%9B%E9%A1%BF%E8%BF%90%E5%8A%A8%E5%AE%9A%E5%BE%8B)
:::

## 组件
这应该才是vuepress的精髓吧

:::: tabs type:card
::: tab 插补
```md
{{ 1 + 1 }}
>> 2
```
:::
::: tab 指令
```md
<span v-for="i in 3">{{ i }} </span>
>> 1 2 3
```
:::
::: tab 网页元数据
```md
{{ $page.frontmatter.title }}
>> 用Vuepress搭建博客
```
:::
::: tab 使用组件
使用任何在`.vuepress/components`下安装的组件
```md
<Badge text="beta" type="warning"/>
```
<Badge text="beta" type="warning"/>
:::
::: tab 自定义组件
```md
<quiz v-bind:quizNum=1 />
```
<quiz v-bind:quizNum=1 />
:::
::::

<!-- ## 图标
我还没弄清楚怎么把`plotly`导进来, 而且要找到`load-json`的办法 -->