'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 3\\018')
'''
import pandas as pd
stock=pd.read_csv('stockszA.csv',index_col='Trddt')
Vanke=stock[stock.Stkcd==2]

close=Vanke.Clsprc
close.head()

close.index=pd.to_datetime(close.index)
close.index.name='Date'
close.head()

lagclose=close.shift(1)
lagclose.head()

Calclose=pd.DataFrame({'close':close,'lagclose':lagclose})
Calclose.head()

simpleret=(close-lagclose)/lagclose
simpleret.name='simpleret'
simpleret.head()
calret=pd.merge(Calclose,pd.DataFrame(simpleret),left_index=True
,right_index=True)
calret.head()

simpleret2=(close-close.shift(2))/close.shift(2)
simpleret2.name='simpleret2'
calret['simpleret2']=simpleret2
calret.head()
calret.iloc[5,:]

import ffn
ffnSimpleret=ffn.to_returns(close)
ffnSimpleret.name='ffnSimpleret'
ffnSimpleret.head()

#假设一年有245个交易日
annualize=(1+simpleret).cumprod()[-1]**(245/311)-1
annualize

def annualize(returns,period):
    if period=='day':
        return((1+returns).cumprod()[-1]**(245/len(returns))-1)
    elif period=='month':
        return((1+returns).cumprod()[-1]**(12/len(returns))-1)
    elif period=='quarter':
        return((1+returns).cumprod()[-1]**(4/len(returns))-1)
    elif period=='year':
        return((1+returns).cumprod()[-1]**(1/len(returns))-1)
    else:
        raise Exception("Wrong period")

import numpy as np
comporet=np.log(close/lagclose)
comporet.name='comporet'
comporet.head()
comporet[5]
ffnComporet=ffn.to_log_returns(close)
ffnComporet.head()
comporet2=np.log(close/close.shift(2))
comporet2.name='comporet2'
comporet2.head()
comporet2[5]

comporet=comporet.dropna()
comporet.head()
sumcomporet=comporet+comporet.shift(1)
sumcomporet.head()

simpleret.plot()
((1+simpleret).cumprod()-1).plot()

#数据日期为2014年1月1日到2014年12月31日
#SAPower代表“航天动力”股票，股票代码为“600343”
#DalianRP代表“大橡塑”股票，股票代码为“600346”

SAPower=pd.read_csv('SAPower.csv',index_col='Date')
SAPower.index=pd.to_datetime(SAPower.index)
DalianRP=pd.read_csv('DalianRP.csv',index_col='Date')
DalianRP.index=pd.to_datetime(DalianRP.index)

returnS=ffn.to_returns(SAPower.Close).dropna()
returnD=ffn.to_returns(DalianRP.Close).dropna()

returnS.std()
returnD.std()

def cal_half_dev(returns):
    mu=returns.mean()
    temp=returns[returns<mu]
    half_deviation=(sum((mu-temp)**2)/len(returns))**0.5
    return(half_deviation)

cal_half_dev(returnS)
cal_half_dev(returnD)

#历史模拟法
returnS.quantile(0.05)
returnD.quantile(0.05)

#协方差矩阵法
from scipy.stats import norm
norm.ppf(0.05,returnS.mean(),returnS.std())
norm.ppf(0.05,returnD.mean(),returnD.std())


returnS[returnS<=returnS.quantile(0.05)].mean()
returnD[returnD<=returnD.quantile(0.05)].mean()

import datetime
r=pd.Series([0,0.1,-0.1,-0.01,0.01,0.02],index=[datetime.date(2015,7,x) for x in range(3,9)])
r
value=(1+r).cumprod()
value
D=value.cummax()-value
D
d=D/(D+value)
d
MDD=D.max()
MDD
mdd=d.max()
mdd
ffn.calc_max_drawdown(value)
ffn.calc_max_drawdown((1+returnS).cumprod())
ffn.calc_max_drawdown((1+returnD).cumprod())