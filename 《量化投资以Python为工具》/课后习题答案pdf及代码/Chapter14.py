# -*- coding: utf-8 -*-

import pandas as pd
#1
Bwages = pd.read_csv('Data/Part2/002/Bwages.csv')
Bwages.wage.hist(normed=True)

Bwages.wage.hist(normed=True,cumulative=True)

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
kde = stats.gaussian_kde(Bwages.wage)
bins=np.linspace(0, 50, num=200)
plt.plot(bins,kde(bins).cumsum())

#2.
history = pd.read_csv('Data/Part2/001/history.csv',
                      index_col = 'Date')
                      
revenue=len(history['Emerging.Markets'][history['Emerging.Markets']>0])

loss=len(history['Emerging.Markets'][history['Emerging.Markets']<0])

p=revenue/(revenue+loss)

1-stats.binom.cdf(6,12,p)

#3.
from math import sqrt
norm_bins=np.linspace(-5, 5, num=200)

plt.plot(norm_bins,stats.norm.pdf(norm_bins,0,1),label='N(0,1)')

plt.plot(norm_bins,stats.norm.pdf(norm_bins,0,sqrt(0.5)),
         label='N(0,0.5)')

plt.plot(norm_bins,stats.norm.pdf(norm_bins,0,sqrt(2)),label='N(0,2)')

plt.plot(norm_bins,stats.norm.pdf(norm_bins,2,1),label='N(2,1)')

plt.legend()

#5.
import numpy as np
sample = np.random.exponential(2,10000)

sample.mean()

sample.var()

#6
import matplotlib.pyplot as plt
log_bins=np.linspace(0, 10, num=200)

plt.plot(log_bins,stats.lognorm.pdf(log_bins,1,0,1))
