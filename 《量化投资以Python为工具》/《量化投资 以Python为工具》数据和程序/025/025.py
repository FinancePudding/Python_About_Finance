'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 4\\025')
'''
import sys
sys.path.append('E:\\book_data\\part 4')
import pandas as pd
from statsmodels.graphics.tsaplots import *
from statsmodels.tsa import stattools
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='C:/Windows/Fonts/msyh.ttf')
import numpy as np
from arch import arch_model


SHret=pd.read_table('TRD_IndexSum.txt',index_col='Trddt',sep='\t')

SHret.index=pd.to_datetime(SHret.index)

SHret=SHret.sort()
#绘制收益率平方序列图
plt.subplot(211)
plt.plot(SHret**2)
plt.xticks([])
plt.title('Squared Daily Return of SH Index')

plt.subplot(212)
plt.plot(np.abs(SHret))
plt.title('Absolute Daily Return of SH Index')

LjungBox=stattools.q_stat(stattools.acf(SHret**2)[1:13],len(SHret))
LjungBox[1][-1]
am = arch_model(SHret)
model = am.fit(update_freq=0)
print(model.summary())