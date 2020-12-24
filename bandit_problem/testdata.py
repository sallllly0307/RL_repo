import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
import datetime

# 指数乱数を発生させる
lam = 0.01
exponential = rd.exponential(0.001/lam, size=100)

# 指数乱数の分布を描画
now = datetime.datetime.now()
plt.hist(exponential, bins=100)
plt.savefig('testdata' + str(now) + '.png')
