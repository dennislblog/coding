'''
目标函数 𝑦=𝑠𝑖𝑛2𝜋𝑥 , 加上一个正态分布的噪音干扰，用M次多项式去拟合
'''
import numpy as np
import scipy as sp
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


# 真实函数
def real_func(x):
    return np.sin(2 * np.pi * x)  # 𝑠𝑖𝑛2𝜋𝑥


# 多项式拟合函数
def fit_func(p, x):
    f = np.poly1d(p)
    return f(x)


# 残差
def residuals_func(p, x, y):
    ret = fit_func(p, x) - y
    return ret

# 带正则化拟合函数, 这里是L2正则
def residuals_func_regularization(p,x,y,lambd=0.0001):
    ret = fit_func(p,x)-y
    ret = np.append(ret, np.sqrt(0.5*lambd*np.square(p)))
    return ret


def fitting(x, x_points, y_, y, M=0):
    p_init = np.random.rand(M + 1)  # 随机初始化多项式参数
    # 最小二乘法
    p_lsq = leastsq(residuals_func, p_init, args=(x, y))
    r_lsq = leastsq(residuals_func_regularization, p_init, args=(x,y))
    print("fitting parameters: ", p_lsq[0])

    # 可视化
    plt.plot(x_points, real_func(x_points), ":", label='真实')
    plt.plot(x_points, fit_func(p_lsq[0], x_points), label='拟合')
    plt.plot(x_points, fit_func(r_lsq[0], x_points), label='正则')
    plt.plot(x, y, 'bo', label='noise')
    plt.title("多项式次数 M=%d" % (M))
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 消除中文乱码
    plt.legend()
    plt.show()
    return p_lsq


if __name__ == '__main__':
    x = np.linspace(0, 1, 15)
    x_points = np.linspace(0, 1, 1000)
    y_ = real_func(x)
    y = [np.random.normal(0, 0.1) + y1 for y1 in y_]  # 加入噪声扰动
    p_lsq_0 = fitting(x, x_points, y_, y, 1)
    p_lsq_1 = fitting(x, x_points, y_, y, 3)
    p_lsq_3 = fitting(x, x_points, y_, y, 5)
    p_lsq_9 = fitting(x, x_points, y_, y, 9)