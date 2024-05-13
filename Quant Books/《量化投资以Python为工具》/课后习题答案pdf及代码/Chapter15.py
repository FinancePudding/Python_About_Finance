# -*- coding: utf-8 -*-
#1.
import numpy as np
import math
from scipy import stats
mu=np.mean((6.683,6.678,6.767,6.692,6.672,6.678))
std=np.std((6.683,6.678,6.767,6.692,6.672,6.678))
low = mu - stats.t.ppf(0.95,5) * std/ math.sqrt(6)
high = mu + stats.t.ppf(0.95,5) * std/ math.sqrt(6)
low
high

mu=np.mean((6.661,6.664,6.668,6.666,6.665))
std=np.std((6.661,6.664,6.668,6.666,6.665))
low = mu - stats.t.ppf(0.95,4) * std/math.sqrt(5)
high = mu + stats.t.ppf(0.95,4) * std/ math.sqrt(5)
low
high

#2.
mu=np.mean((5.9,7.3,6.6,5.8,5.7,5.3,5.9,7,6.5))
std=np.std((5.9,7.3,6.6,5.8,5.7,5.3,5.9,7,6.5))
low = mu - stats.t.ppf(0.975,8) * std/3
high = mu + stats.t.ppf(0.975,8) * std/3
low
high

#5.
import pandas as pd
import matplotlib.pyplot as plt
Bwages = pd.read_csv('Data/Part2/002/Bwages.csv')
stats.ttest_1samp(Bwages.wage,0)
Bwages.wage.hist(normed=True)
mu = Bwages.wage.mean()
std = Bwages.wage.std()
low = mu - stats.t.ppf(0.975,len(Bwages)-1) * std / math.sqrt(len(Bwages))
high = mu + stats.t.ppf(0.975,len(Bwages)-1) * std / math.sqrt(len(Bwages))
low
high

#6.
Bwages.wage.hist(normed=True) 
bins=np.linspace(0,50,200)
plt.plot(bins,stats.norm.pdf(bins,mu,std))

#7.
from scipy import stats
MT=(0.225,0.262,0.217,0.24,0.23,0.229,0.235,0.217)
Sn=(0.209,0.205,0.196,0.21,0.202,0.207,0.224,0.223)
stats.ttest_ind(MT,Sn)

#8.
from scipy import stats
region1=(168,180,181,172,165,160,166,165,177,174) 
region2=(169,170,176,173,166,167,166,173,171,170)
stats.ttest_ind(region1,region2)

#9.
import pandas as pd
from scipy import stats
Bwages = pd.read_csv('Data/Part2/002/Bwages.csv')
stats.ttest_1samp(Bwages.wage,11)

#10.
import pandas as pd
from scipy import stats
history = pd.read_csv('Data/Part2/001/history.csv',
                      index_col = 'Date')

stats.ttest_ind(history['Emerging.Markets'],
	history['Global.Macro'])
#11.
stats.ttest_rel(history['Emerging.Markets'],
	history['Global.Macro'])
