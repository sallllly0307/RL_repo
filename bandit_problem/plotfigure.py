import os
import numpy as np
import pandas as pd
import numpy.random as rd
import matplotlib.pyplot as plt
import datetime
from bandit import exponential

now = datetime.datetime.now()
plt.hist(exponential, bins=15)
plt.savefig('testdata' + str(now) + '.png')
