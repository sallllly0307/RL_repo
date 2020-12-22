import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt

# 指数乱数を発生させる
lam = 0.1
exponential = rd.exponential(0.1/lam, size=100)
