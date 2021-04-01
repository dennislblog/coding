---
title: 卷积神经网络
date: 2021-03-20
autoGroup-3: 深度学习
tags:
  - Knowledge
---

::: tip
在这里记录LeNet, AlexNet, VGG, GoogleNet, ResNet, DenseNet, SENet和MobileNet异同
:::

## LeNet

:::: tip
由LeCun于1998年提出, 用于解决手写数字识别任务. 组成元素包括卷积层、池化层、全连接层

> ![LeNet](~@assets/ml_cnn-1.png)
> 1. 输入一个`28 x 28`的图像, 用`np.pad`填充至`32 x 32`
> 2. 经过尺寸为`5 x 5`, 步长为`1`, 卷积核数目为`6`的卷积层后, 图像尺寸变为`32-5+1=28`, 即`28 x 28 x 6`
> 3. 第一个池化核尺寸为`2 x 2`(batch, height, width, channel), 步长为`2`(batch, stride, stride, channel), 池化后图像尺寸减半, 变为`14 x 14 x 6`
> 4. 第二个卷积核尺寸为`5 x 5`, 步长为`1`, 卷积核数目为`16`, 图像尺寸变为`14-5+1=10`, 即`28 x 28 x 16`
> 5. 第二个池化核同前面那个池化层一样, 图像尺寸减半得到`5x5x16`
> 6. 最后几个全连接层得到`25 x 16 -> 120 -> 84 -> 10`, 激活函数都是relu


::: details 代码
<<< docs/codes/LeNet.py
:::

::::

## AlexNet

:::: tip
2012年，Alex Krizhevsky, Ilya Sutskever, Geoff Hinton等人设计出了AlexNet，夺得了2012年ImageNet LSVRC的冠军, 错误率15.3%远超过第二名的26.2%
> ![LeNet](~@assets/ml_cnn-2.png#center)
> 1. 包含5层卷积层和三层全连接层, 相比LeNet增加了深度, 使用了线性激活函数`ReLU`, 使用了`Dropout`,`Data Augmentation`这些防止过拟合的办法
> 2. 相比`sigmoid/tanh`, 由于`ReLU`是线性的, 导数始终是`1`, 计算量大大减少, 收敛速度会加快不少, 而且避免了梯度消失(sigmoid在很多地方导数接近$0$)
> 3. 数据扩充(data augmentation)指的是通过对原始数据(比如照片)进行一些翻转, 随机裁剪, 平移, 光照变化等, 改变输入数据, 但输出结果仍然不变, 相当于增加训练数据, 提高算法准确率
> 4. 重叠池化(overlapping pooling), 传统池化是不重叠的, AlexNet要求池化窗口移动的步长小于窗口长度, 这样压缩没有以前厉害, 所以多加了几层?
> 5. 局部归一(local response normalization), 因为`ReLU`的响应结果是无界的(无穷大), 通过抑制同一位置其他通道的特征值来抑制过拟合. 貌似就是让兴奋的更加兴奋, 如果周围所有神经元都很兴奋, 则归一化处理后数值上都不那么兴奋了
> 6. Dropout, 在深度学习网络的训练过程中, 按照一定的概率将一些神经元**暂时**从网络中丢弃. 由于是随机丢弃, 故而每一个batch都在训练不同的网络, 相当于集成学习

::: details 代码
<<< docs/codes/AlexNet.py
:::
::::








## 参考资料

[1] [你应该知道的几种CNN网络与实现](https://zhuanlan.zhihu.com/p/176987177)

[2] [卷积神经网络介绍](https://easyfly007.github.io/blogs/index.html)

[3] [大话CNN经典模型：AlexNet](https://my.oschina.net/u/876354/blog/1633143)