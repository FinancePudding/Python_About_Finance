'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 3\\020')
'''

import pandas as pd
indexcd=pd.read_csv('TRD_Index.csv',index_col='Trddt')
mktcd=indexcd[indexcd.Indexcd==902]
mktcd.head()
mktret=pd.Series(mktcd.Retindex.values,index=pd.to_datetime(mktcd.index))
mktret.name='mktret'
mktret.head()
mktret=mktret['2014-01-02':'2014']
mktret.tail()
xin_an=pd.read_csv('xin_an.csv',index_col='Date')
xin_an.index=pd.to_datetime(xin_an.index)
xin_an.head()
xin_an=xin_an[xin_an.Volume!=0]
xin_anret=(xin_an.Close-xin_an.Close.shift(1))/xin_an.Close.shift(1)
xin_anret.name='returns'
xin_anret=xin_anret.dropna()
xin_anret.head()
xin_anret.tail()
Ret=pd.merge(pd.DataFrame(mktret),
             pd.DataFrame(xin_anret),
left_index=True,right_index=True,how='inner')
rf=1.036**(1/360)-1
rf
Eret=Ret-rf
Eret.head()
import matplotlib.pyplot as plt
plt.scatter(Eret.values[:,0],Eret.values[:,1])
plt.title('XinAnGuFen return and market return')

import statsmodels.api as sm
model=sm.OLS(Eret.returns[1:],sm.add_constant(Eret.mktret[1:]))
result=model.fit()
result.summary()