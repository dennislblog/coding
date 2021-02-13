---
title: TensorFlow 2.0
date: 2021-02-08
autoGroup-2: 工具学习
tags:
  - Knowledge
sidebarDepth: 3
---

::: tip
在这里记录TensorFlow 2.0的知识
:::

<!-- more -->

## Basic Operation

### constant, concat, square
__问题__： 算相邻质数的平方差的绝对值, 例如$|2^2 - 3^2| = 5$

```python
prime_numbers = tf.constant([2, 3, 5, 7, 11, 13, 17, 19, 23])
shifted_prime_numbers = tf.concat([prime_numbers[1:], [29]], axis=0)
diffs = tf.abs(tf.square(prime_numbers) - tf.square(shifted_prime_numbers))
```


### random, cast, math, concat
__问题__： 把抛一个6面筛子和一枚硬币的结果存到`[10,3]`的张量中, 第一列是硬币结果, 第二列是筛子结果, 第三列为如果硬币是头且筛子大于$3$的情况, 例如其中一行是`[1,4,1]`

```python
dtype = tf.int32
flip_head = tf.random.uniform([10, 1], maxval=2, dtype=dtype)
die_number = tf.random.uniform([10, 1], minval=1, maxval=7, dtype=dtype)
big_than_three = tf.cast(tf.math.greater(die_number, 3), dtype)
success = tf.cast(tf.math.equal(big_than_three + flip_head, 2), dtype)
simulation_result = tf.concat([coin_flip, die_number, success], axis=1)
```

### expand_dims, tile, reshape
__问题__： 计算两个向量$S_1 \in \mathbb{R}^{m\times d}$ 和 $S_2 S_1 \in \mathbb{R}^{n\times d}$ 的欧几里得距离(注意这两个向量的长度不一样)

```python
def euclidean_norm_distance(v, w):
    # 假设 v.shape = (3,5) and w.shape = (2,5)
    n, _ = tf.shape(v); m, _ = tf.shape(w)
    # expand_dim: 插入一个维度; tile: 某个维度重复
    v = tf.tile(tf.expand_dims(v, 1), [1,m,1]) 
    w = tf.tile(tf.expand_dims(w,0),[n,1,1])
    # 求距离: (3,2,5) -> (3,2)
    distances = tf.math.reduce_sum((v-w)**2, axis=2)
    distances = tf.math.sqrt(distances)
    # 每一行正则化: (3) -> (3,1)
    row_sum = tf.reshape(tf.math.reduce_sum(distances, axis=1), [-1,1])
    return distances / row_sum
```


## Eager Execution

TensorFlow 的 Eager Execution 是一种命令式编程环境，可立即评估操作，无需构建图：操作会返回具体的值，而不是指向计算图节点的指针. 因此我们可以直接`print(tensor)`
```python
a = tf.constant([[1,9],[3,6]])
b = tf.add(a,2)
s = np.multiply(a,b)        #可以当做numpy数据用
print(a.numpy())
```
Eager Execution的一个主要好处是在执行模型时可以使用宿主语言(Python)的所有功能. 比如这里的取余是在`tensor`上完成的
```python
max_num = tf.convert_to_tensor(16)
for num in range(1, max_num.numpy() + 1):
    num = tf.constant(num)
    if int(num % 3) == 0: print('buzz')
```

### gradient, apply_gradient
在 Eager Execution中，使用 `tf.GradientTape` 来跟踪操作以便稍后计算梯度. `tape.gradient`读取所有记录在这盘磁带的前向传播操作, 用`optimizer.apply_gradient`反向播放磁带, 用完后把磁带丢弃, 下次需要重新创建一盘磁带
::::: tabs type: card
:::: tab mnist
```python{10,14}
""" 优化器与损失函数 """
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss_history = []
"""
(images, labels): [32, 28, 28, 1], [32]
logits:           [32, 10]
mnist_model.trainable_variables: [3, 3, 1, 16] x 6 (list)
"""
for (batch, (images, labels)) in enumerate(dataset.take(400)):
    with tf.GradientTape() as tape:
        logits = mnist_model(images, training=True)
        loss_value = loss_object(labels, logits)
    loss_history.append(loss_value.numpy().mean())
    grads = tape.gradient(loss_value, mnist_model.trainable_variables)
    optimizer.apply_gradients(zip(grads, mnist_model.trainable_variables))
```
::: details loss变化
![](~@assets/ml_tensorflow-1.png#center)
:::
::::
:::: tab y = 3x + 2
```python{4-5,15,17}
class Regression(tf.keras.Model):
    def __init__(self):
        super(Regression, self).__init__()
        self.W = tf.Variable(5., name='weight')
        self.B = tf.Variable(10., name='bias')
    def call(self, inputs):
        return inputs * self.W + self.B
x = tf.random.normal([2000]); noise = tf.random.normal([2000])
y = x * 3 + 2 + noise

def loss(model, inputs, targets):
    error = model(inputs) - targets
    return tf.reduce_mean(tf.square(error))
def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, [model.W, model.B])

model = Regression()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)
for i in range(300):
    grads = grad(model, training_inputs, training_outputs)
    optimizer.apply_gradients(zip(grads, [model.W, model.B]))
    if i % 20 == 0:  print(f"loss: {loss(model, x, y):.3f}")
```
::: details 数据拟合
![](~@assets/ml_tensorflow-2.png#center)
:::
::::
:::::

### checkpoint, assign, call

:::: tabs type: card
::: tab 生命周期
之前的变量生命周期是由`tf.Session`控制, 但在`Eager Execution`状态下, 状态对象的生命周期由其对应的 Python 对象的生命周期决定
```python{6}
"""将tf.Variable保存到检查点, 并从中恢复"""
x = tf.Variable(6.0); root = tf.train.Checkpoint(x=x)
x.assign(1.0); root.save('./ckpt/')   #保存检查点
x.assign(8.0); root.restore(tf.train.latest_checkpoint('./ckpt/')) #读取检查点
print(x)
>> <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=1.0>

"""常用来保存模型和优化器"""
root = tf.train.Checkpoint(optimizer=optimizer,model=model)
# root.save(path) root.restore(tf.train.latest_checkpoint(path))
```
:::
::: tab 模型保存/恢复
```python
""" 保存权重 """
model.save_weights('./weights/model'); model.load_weights('./weights/model')
model.save_weights('./model.h5', save_format='h5'); model.load_weights('./model.h5')
""" 保存网络结构 """
json_str = model.to_json(); model = tf.keras.models.model_from_json(json_str)
yaml_str = model.to_yaml(); model = tf.keras.models.model_from_yaml(yaml_str)
""" 保存整个模型 """
model.save('model.h5'); model = tf.keras.models.load_model('model.h5')
```
:::
::::

tf.keras.metrics存储为对象, 通过将新数据传递给callable来更新度量标准
```python
m = tf.keras.metrics.Mean('loss')
m(0); m(1); m(5)
print(m.result()) # => 2.0
m([10,4])
print(m.result()) # => 4.0
```

### gpu, cpu
```python
import time
def measure(x, steps):
    tf.matmul(x, x); start = time.time()
    for i in range(steps):
        x = tf.matmul(x, x)
    _ = x.numpy()
    end = time.time(); return end - start

with tf.device("/cpu:0"):
    print("CPU: {} secs".format(measure(tf.random.normal(shape), steps)))
with tf.device("/gpu:0"):
    print("GPU: {} secs".format(measure(tf.random.normal(shape), steps)))
>> CPU: 1.698425054550171 secs
>> GPU: 0.13264727592468262 secs
""" 也可以使用 tensor.cpu() tensor.gpu() 的方法搬运对象 """
```

### watch
1. TensorFlow默认是会把`tf.Variable`和`tf.keras`里模型参数给自动加到被追踪的磁带`tf.GradientTape`里面, 下面的`tf.constant(100.)`不属于这个范围, 因此我们这里需要加`tape.watch(x)`强制追踪
2. 自定义梯度可以提供数值稳定的梯度, 比如下面这个例子, 如果不加自定义梯度, 会出错
:::: tabs type: card
::: tab 不加
$$y = \log\left(1+ e^x \right)$$
```python
def log1pexp(x):
    return tf.math.log(1 + tf.exp(x))
def grad_log1pexp(x):
    with tf.GradientTape() as tape:
        tape.watch(x); value = log1pexp(x)
    return tape.gradient(value, x)
print(grad_log1pexp(tf.constant(0.)).numpy())   # => 0.5 是对的
print(grad_log1pexp(tf.constant(100.)).numpy()) # => nan 不对
```
:::
::: tab 自定义
```python
@tf.custom_gradient
def log1pexp(x):
    def grad(dy):
        return dy * (1 - 1 / (1 + tf.exp(x)))
    return tf.math.log(1 + tf.exp(x)), grad
def grad_log1pexp(x):
    with tf.GradientTape() as tape:
        tape.watch(x); value = log1pexp(x)
    return tape.gradient(value, x)
print(grad_log1pexp(tf.constant(0.)).numpy())   # => 0.5 是对的
print(grad_log1pexp(tf.constant(100.)).numpy()) # => 1.0 也是对的
```
:::
::: tab 梯度限制
```python
@tf.custom_gradient
def clip_gradient_by_norm(x, norm):
    y = tf.identity(x) # same shape and contents as x
    def grad_fn(dresult):
        return [tf.clip_by_norm(dresult, norm), None]
    return y, grad_fn
```
:::
::::


## Keras

TensorFlow 2.0推荐使用`tf.keras`构建网络，常见的神经网络都包含在`tf.keras.layer`中

### model and layer

:::: tabs type: card
::: tab 简单堆叠模型
```python
model = tf.keras.Sequential()
model.add(layers.Dense(32, activation='relu', kernel_initializer=tf.keras.initializers.glorot_normal))
model.add(layers.Dense(10, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
```
:::
::: tab 自定义模型
- 在`__init__ `方法中创建层并将它们设置为类实例的属性。
- 在`__call__`方法中定义前向传播
```python
class Custom_Model(tf.keras.Model):
    def __init__(self, num_classes=10):
        super(Model, self).__init__(name='my_model')
        self.num_classes = num_classes
        self.layer1 = layers.Dense(32, activation='relu', kernel_initializer=tf.keras.initializers.glorot_normal)
        self.layer2 = layers.Dense(num_classes, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(0.01))
    def call(self, inputs):
        h1 = self.layer1(inputs)
        out = self.layer2(h1)
        return out
model = Custom_Model(num_classes=10)
```
:::
::: tab 自定义层
- `__init__`: (可选)定义该层要使用的子层
- build：创建层的权重。使用 add_weight 方法添加权重。
- call：定义前向传播。
```python
class Custom_Layer(layers.Layer):
    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(Custom_Layer, self).__init__(**kwargs)
    def build(self, input_shape):
        shape = tf.TensorShape((input_shape[1], self.output_dim))
        self.kernel = self.add_weight(name='kernel1', shape=shape,
         initializer='uniform', trainable=True)
        super(Custom_Layer, self).build(input_shape)
    def call(self, inputs):
        return tf.matmul(inputs, self.kernel)
model = tf.keras.Sequential([Custom_Layer(10), layers.Activation('softmax')])
```
::::

- 激活函数： 可以是字符串"sigmoid", 也可以是函数`tf.sigmoid`
- 创建层权重（核和偏置）的初始化方案, 默认是`Glorot Uniform` (kernel_initializer 和 bias_initializer)
- 应用层权重（核和偏置）的正则化方案, 例如`l1, l2`正则化 (kernel_regularizer 和 bias_regularizer)

构建好模型后，通过调用 compile 方法配置该模型的学习流程
```python
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
             loss=tf.keras.losses.categorical_crossentropy,
             metrics=[tf.keras.metrics.categorical_accuracy])
```

### batch, repeat, from_tensor_slices
:::: tabs type: card
::: tab numpy 数据
对于小型数据集，可以使用Numpy构建输入数据。
```python
"""
train_x, train_y: [1000,72], [1000, 10]
val_x, train_y:   [200,72], [200, 10]
"""
model.fit(train_x, train_y, epochs=10, batch_size=100, validation_data=(val_x, val_y))
```
在`model fit`一个数据集以后, 网络图就被建立了, 我们就可以用`model.summary()`来查看网络结构
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense_4 (Dense)              (100, 32)                 2336      
_________________________________________________________________
dense_5 (Dense)              (100, 10)                 330       
=================================================================
Total params: 2,666
Trainable params: 2,666
Non-trainable params: 0
```
:::
::: tab tf.data 数据
对于大型数据集可以使用tf.data构建训练输入。
```python
x = np.arange(1,10).reshape(3,3)
dataset = tf.data.Dataset.from_tensor_slices((x, x))
list(dataset.as_numpy_iterator())
"""
    [(array([1, 2, 3]), array([1, 2, 3])),
     (array([4, 5, 6]), array([4, 5, 6])),
     (array([7, 8, 9]), array([7, 8, 9]))]
"""
```
原本只有$1000$个训练数据, $200$个验证数据, 但模型训练我要做$10$个`epoch`, 每个`epoch`有$30$个`batch`训练, 这样总共需要$300$个`batch`, 这里我们通过调用`repeat()`函数无限产生`batch`来满足训练需求
```python{8,10}
"""
val_x, train_y:   ([200,72], [200, 10])
dataset:          ([72, 10]) x 200
batch(32):        ([32, 72], [32, 10]) x 7
repeat():         ([32, 72], [32, 10]) x infty
"""
dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
dataset = dataset.batch(32); dataset = dataset.repeat()
val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
val_dataset = val_dataset.batch(32); val_dataset = val_dataset.repeat()
model.fit(dataset, epochs=10, steps_per_epoch=30,
    validation_data=val_dataset, validation_steps=3)
test_data = tf.data.Dataset.from_tensor_slices((test_x, test_y))
test_data = test_data.batch(32).repeat()
model.evaluate(test_data, steps=10)   #每batch有32个(x,y), 总共10次
>> 79.86, 0.091 # loss value and accuracy
```
:::
::::

### callback
我们可以编写自己的自定义回调，或使用tf.keras.callbacks中的内置函数
- `tf.keras.callbacks.ModelCheckpoint`：定期保存模型的检查点。
- `tf.keras.callbacks.LearningRateScheduler`：动态更改学习率。
- `tf.keras.callbacks.EarlyStopping`：验证性能停止提高时进行中断培训。
- `tf.keras.callbacks.TensorBoard`：使用TensorBoard监视模型的行为 。

```python{5-6}
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs')
]
model.fit(train_x, train_y, batch_size=16, epochs=5,
    callbacks=callbacks, validation_data=(val_x, val_y))
```

