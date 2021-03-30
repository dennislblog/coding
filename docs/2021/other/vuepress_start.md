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
一个由VuePress生成的网站，它是用Vue、Vue-router、Webpack以及利用服务端渲染(SSR)而来, 它不仅支持Vue组件的写法, 还内置Stylus语法
:::

<!-- more -->


## 支持Tex语法

$$\begin{aligned}
  a&=b+c \cr
  d+e&=f \\[1em]
     &=\Big( r(s,a) + \gamma V^*(s') \Big)
\end{aligned}$$

## 支持MultiTabs操作

:::: tabs type: card
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
Vue <Badge text="2.5.0+"/> 
Vuex <Badge text="beta" type="warn" vertical="top"/> 
Vue-Resource<Badge text="废弃" vertical="middle" type="error"/>
```
<Badge text="beta" type="warning"/> Vue <Badge text="2.5.0+"/> Vuex <Badge text="beta" type="warn" vertical="top"/> Vue-Resource<Badge text="废弃" vertical="middle" type="error"/>
:::
::: tab 自定义组件
```md
<quiz :quizNum=1 />
```
<quiz :quizNum=1 />
:::
::::

## 图表
我还没弄清楚怎么把`plotly`导进来, 而且要找到`load-json`的办法, 暂时使用的[chart.js](https://www.chartjs.org/docs/latest/charts/line.html)

<!-- <test-vue/> -->


## 链接

所有`.md`文件中的标题(例如h2和h3)都自动添加了锚点链接, 可以根据与当前文件相对路径的关系编辑跳转链接, 例如在这里我们要跳回到[本文开头](./vuepress_start/#支持Tex语法)


## 比较

<pros-cons
  intro="There are a couple of things we need to cover:"
  :good="[
    'Documentation Theme Based on Vue.',
    'Use of markdown-it plugins.',
    'Static Site Generator.'
  ]"
  :bad="[
    'Vuepress is not very stable yet',
    'Can be complex to configure',
  ]"
/>

## 参考资料

[1] [Vuepress](https://wangtunan.github.io/blog)