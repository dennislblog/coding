import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron
import matplotlib.pyplot as plt


class PerceptronModel():
    def __init__(self, X, y, eta):
        self.w = np.zeros(len(X[0]), dtype=np.float)  # 权重
        self.b = 0  # 偏置
        self.eta = eta  # 学习率
        self.dataX = X  # 数据
        self.datay = y  # 标签
        self.iterTimes = 0  # 迭代次数

        # 对偶形式的参数
        self.a = np.zeros(len(X), dtype=np.float)  # alpha
        self.Gmatrix = np.zeros((len(X), len(X)), dtype=np.float)
        self.calculateGmatrix()  # 计算Gram矩阵

    def sign0(self, x, w, b):  # 原始形式sign函数
        y = np.dot(w, x) + b
        return y

    def sign1(self, a, G_j, Y, b):  # 对偶形式sign函数
        y = np.dot(np.multiply(a, Y), G_j) + b
        return y

    def OriginClassifier(self):  # 原始形式的分类算法
        self.iterTimes = 0
        self.b = 0
        stop = False
        while not stop:
            wrong_count = 0
            for i in range(len(self.dataX)):
                X = self.dataX[i]
                y = self.datay[i]
                if (y * self.sign0(X, self.w, self.b)) <= 0:
                    self.w += self.eta * np.dot(X, y)
                    self.b += self.eta * y
                    wrong_count += 1
                    self.iterTimes += 1
            if wrong_count == 0:
                stop = True
        print("原始形式，分类完成！步长：%.4f, 共迭代 %d 次" % (self.eta, self.iterTimes))

    def calculateGmatrix(self):  # 计算Gram矩阵
        for i in range(len(self.dataX)):
            for j in range(0, i + 1):  # 对称的计算一半就行
                self.Gmatrix[i][j] = np.dot(self.dataX[i], self.dataX[j])
                self.Gmatrix[j][i] = self.Gmatrix[i][j]

    def DualFormClassifier(self):  # 对偶形式分类算法
        self.iterTimes = 0
        self.b = 0
        stop = False
        while not stop:
            wrong_count = 0
            for i in range(len(self.dataX)):
                y = self.datay[i]
                G_i = self.Gmatrix[i]
                if (y * self.sign1(self.a, G_i, self.datay, self.b)) <= 0:
                    self.a[i] += self.eta
                    self.b += self.eta * y
                    wrong_count += 1
                    self.iterTimes += 1
            if wrong_count == 0:
                stop = True
        print("对偶形式，分类完成！步长：%.4f, 共迭代 %d 次" % (self.eta, self.iterTimes))


def compare_learning_rate(X, y):
    # ------------------学习率不同，查看迭代次数----------------------------
    n = 5; i = 0
    eta_iterTime = np.zeros((n, 3), dtype=float)
    for eta in np.linspace(0.01, 1.01, n):
        eta_iterTime[i][0] = eta  # 第一列，学习率
        perceptron = PerceptronModel(X, y, eta)
        perceptron.OriginClassifier()
        eta_iterTime[i][1] = perceptron.iterTimes  # 第二列，原始算法迭代次数
        perceptron.DualFormClassifier()
        eta_iterTime[i][2] = perceptron.iterTimes  # 第三列，对偶算法迭代次数
        i += 1
    x = eta_iterTime[:, 0]  # 数据切片
    y0 = eta_iterTime[:, 1]
    y1 = eta_iterTime[:, 2]
    plt.scatter(x, y0, c='r', marker='o', label='原始算法')
    plt.scatter(x, y1, c='b', marker='x', label='对偶算法')
    plt.xlabel('步长(学习率)')
    plt.ylabel('迭代次数')
    plt.title("不同步长，不同算法形式下，迭代次数")
    plt.legend()
    plt.show()

def sklearn(X, y):
    # ------------------sklearn实现----------------------------
    classify = Perceptron(fit_intercept=True, max_iter=10000, shuffle=False, eta0=0.5, tol=None)
    classify.fit(X, y)
    print("特征权重：", classify.coef_)  # 特征权重 w
    print("截距（偏置）:", classify.intercept_)  # 截距 b

    # 可视化
    plt.scatter(df[:50][iris.feature_names[0]], df[:50][iris.feature_names[1]], label=iris.target_names[0])
    plt.scatter(df[50:100][iris.feature_names[0]], df[50:100][iris.feature_names[1]], label=iris.target_names[1])
    plt.xlabel(iris.feature_names[0])
    plt.ylabel(iris.feature_names[1])

    # 绘制分类超平面
    x_points = np.linspace(4, 7, 10)
    y = -(classify.coef_[0][0] * x_points + classify.intercept_) / classify.coef_[0][1]
    plt.plot(x_points, y, 'r', label='sklearn Perceptron分类线')

    plt.title("sklearn内置感知机分类")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # 读取鸢尾花数据
    iris = load_iris()
    # 将鸢尾花4个特征，以4列存入pandas的数据框架
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    # 在最后一列追加 加入标签（分类）列数据
    df['lab'] = iris.target

    # df.columns=[iris.feature_names[0], iris.feature_names[1], iris.feature_names[2], iris.feature_names[3], 'lab']
    # df['lab'].value_counts()
    # 选取前两种花进行划分（每种数据50组）
    plt.scatter(df[:50][iris.feature_names[0]], df[:50][iris.feature_names[1]], label=iris.target_names[0])
    plt.scatter(df[50:100][iris.feature_names[0]], df[50:100][iris.feature_names[1]], label=iris.target_names[1])
    plt.xlabel(iris.feature_names[0])
    plt.ylabel(iris.feature_names[1])

    # 选取数据,前100行，前两个特征，最后一列标签
    data = np.array(df.iloc[:100, [0, 1, -1]])
    # X是除最后一列外的所有列，y是最后一列
    X, y = data[:, :-1], data[:, -1]
    # 生成感知机的标签值，+1， -1, 第一种-1，第二种+1
    y = np.array([1 if i == 1 else -1 for i in y])

    # 调用感知机进行分类，学习率eta
    perceptron = PerceptronModel(X, y, eta=0.1)
    perceptron.OriginClassifier()  # 原始形式分类

    # 绘制原始算法分类超平面
    x_points = np.linspace(4, 7, 10)
    y0 = -(perceptron.w[0] * x_points + perceptron.b) / perceptron.w[1]
    plt.plot(x_points, y0, 'r', label='原始算法分类线')

    perceptron.DualFormClassifier()  # 对偶形式分类
    # 由alpha，b 计算omega向量
    omega0 = sum(perceptron.a[i] * y[i] * X[i][0] for i in range(len(X)))
    omega1 = sum(perceptron.a[i] * y[i] * X[i][1] for i in range(len(X)))
    y1 = -(omega0 * x_points + perceptron.b) / omega1

    # 绘制对偶算法分类超平面
    plt.plot(x_points, y1, 'b', label='对偶算法分类线')

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 消除中文乱码
    plt.legend()
    plt.show()

    