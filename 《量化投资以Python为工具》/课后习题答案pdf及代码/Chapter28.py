# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

#1.
pufa = pd.read_csv('Data/Part5/002/problem28-1.csv',
                index_col='date')
                
pufa.index.name='Date'
pufa.index = pd.to_datetime(pufa.index,format='%Y-%m-%d')

mom6_1 = pufa.Close - pufa.Close.shift(6)
mom6_2 = (pufa.Close - pufa.Close.shift(6))/pufa.Close.shift(6)

mom30_1 = pufa.Close - pufa.Close.shift(30)
mom30_2 = (pufa.Close - pufa.Close.shift(30))/pufa.Close.shift(30)

mom90_1 = pufa.Close - pufa.Close.shift(90)
mom90_2 = (pufa.Close - pufa.Close.shift(90))/pufa.Close.shift(90)

def getSignal(x):
    signal = np.where(x>0,1,np.where(x<0,-1,0))
    return(signal)    
signal6 = getSignal(mom6_2)
signal30 = getSignal(mom30_2)
signal90 = getSignal(mom90_2)

ret = (pufa.Close-pufa.Close.shift(1))/pufa.Close.shift(1)
ret6 = ret[6:]
ret30 = ret[30:]
ret90 = ret[90:]

signal6 = pd.Series(signal6[6:],index=ret6.index)
Mom6Ret = ret6[1:] * signal6.shift(1)[1:]

signal30 = pd.Series(signal6[30:],index=ret30.index)
Mom30Ret = ret30[1:] * signal30.shift(1)[1:]

signal90 = pd.Series(signal6[90:],index=ret90.index)
Mom90Ret = ret90[1:] * signal90.shift(1)[1:]


winrate6 = sum(Mom6Ret>0)/sum(Mom6Ret!=0)
winrate6

winrate30 = sum(Mom30Ret>0)/sum(Mom30Ret!=0)
winrate30

winrate90 = sum(Mom90Ret>0)/sum(Mom90Ret!=0)
winrate90

#2.
def getSignal(x):
    first = x.iloc[:,0]
    second = x.iloc[:,1]
    signal = [1 if first[i]>0 and second[i]>0 else -1 if first[i]<0 and second[i]<0 else 0 for i in range(len(first))]
    return(signal)
    
momen = pd.concat([mom6_2,mom90_2],1)
momen = momen.dropna()

signal = getSignal(momen)
signal = pd.Series(signal,index= mom90_2.dropna().index)

MomRet = ret90[2:] * signal.shift(2)[2:]

sum(MomRet>0)/sum(MomRet!=0)

#3.
import pandas as pd
import numpy as np
prices = pd.read_csv('Data/Part5/002/problem28-3.csv',
                index_col='date')                
prices.index.name='Date'
prices.index = pd.to_datetime(prices.index,format='%Y-%m-%d')

prices = prices.asfreq('M',how='end',method='ffill')
ret_pf = (prices.pfyh - prices.pfyh.shift(3))/prices.pfyh.shift(3)
ret_zg = (prices.zgyh - prices.zgyh.shift(3))/prices.zgyh.shift(3)
ret_ms = (prices.msyh - prices.msyh.shift(3))/prices.msyh.shift(3)
ret_gs = (prices.gsyh - prices.gsyh.shift(3))/prices.gsyh.shift(3)
ret_js = (prices.jsyh - prices.jsyh.shift(3))/prices.jsyh.shift(3)


cash = np.ones(len(ret_pf))*1000000
stock = np.zeros(len(ret_pf))

for i in range(4,len(cash)):
    momen = pd.Series([ret_gs[i-1],ret_js[i-1],ret_ms[i-1],ret_pf[i-1],ret_zg[i-1]])
    if i!=4:
        momen_lag = pd.Series([ret_gs[i-2],ret_js[i-2],ret_ms[i-2],ret_pf[i-2],ret_zg[i-2]])
        cash[i] = cash[i-1] + 10000 * prices.iloc[:,momen_lag.idxmax()][i]
    stock[i] = 10000 * prices.iloc[:,momen.idxmax()][i]
    cash[i] -= 10000 * prices.iloc[:,momen.idxmax()][i]

(cash[35]+stock[35]-1000000)/1000000*len(cash)

