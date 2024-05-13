'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 4\\023')
'''

import pandas as pd
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *
import matplotlib.pyplot as plt
import math
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='C:\Windows\Fonts\msyh.ttf')
import numpy as np
from arch.unitroot import ADF

#读取数据
data=pd.read_table('TRD_Index.txt',sep='\t',index_col='Trddt')
data.head()
# test=data.Clsindex
#提取上证综指数据
SHindex=data[data.Indexcd==1]
#转换成时间序列类型
SHindex.index=pd.to_datetime(SHindex.index)
SHRet=SHindex.Retindex
type(SHRet)
SHRet.head()
SHRet.tail()
#计算自相关系数
acfs=stattools.acf(SHRet)
acfs[:5]
#绘制自相关系数图
plot_acf(SHRet,use_vlines=True,lags=30)
#计算偏自相关系数
pacfs=stattools.pacf(SHRet)
pacfs[:5]
plot_pacf(SHRet,use_vlines=True,lags=30)

SHclose=SHindex.Clsindex
SHclose.plot()
plt.title('2014-2015 年 上 证 综 指 收 盘 指 数 时 序 图 ')

SHRet.plot()
plt.title('2014-2015年上证综指收益率时序图')

plot_acf(SHRet,use_vlines=True,lags=30)
plot_pacf(SHRet,use_vlines=True,lags=30)
plot_acf(SHclose,use_vlines=True,lags=30)

adfSHRet=ADF(SHRet)
print(adfSHRet.summary().as_text())
adfSHclose=ADF(SHclose)
print(adfSHclose.summary().as_text())


#生成纯随机序列
whiteNoise=np.random.standard_normal(size=500)
#绘制序列图
plt.plot(whiteNoise,c='b')
plt.title('White Noise')

LjungBox1=stattools.q_stat(stattools.acf(SHRet)[1:13],len(SHRet))
LjungBox1
LjungBox1[1][-1]

LjungBox2=stattools.q_stat(stattools.acf(SHclose)[1:13],len(SHRet))
LjungBox2[1][-1]

