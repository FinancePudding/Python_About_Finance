# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
def rsi(price,period=6):
    import pandas as pd
    clprcChange=price-price.shift(1)
    clprcChange=clprcChange.dropna()
    indexprc=clprcChange.index
    upPrc=pd.Series(0,index=indexprc)
    upPrc[clprcChange>0]=clprcChange[clprcChange>0]
    downPrc=pd.Series(0,index=indexprc)
    downPrc[clprcChange<0]=-clprcChange[clprcChange<0]
    rsidata=pd.concat([price,clprcChange,upPrc,downPrc],\
    axis=1)
    rsidata.columns=['price','PrcChange','upPrc','downPrc']
    rsidata=rsidata.dropna();
    SMUP=[]
    SMDOWN=[]
    for i in range(period,len(upPrc)+1):
        SMUP.append(np.mean(upPrc.values[(i-period):i],\
        dtype=np.float32))
        SMDOWN.append(np.mean(downPrc.values[(i-period):i],\
        dtype=np.float32))
        rsi=[100*SMUP[i]/(SMUP[i]+SMDOWN[i]) \
        for i in range(0,len(SMUP))]
    indexRsi=indexprc[(period-1):]
    rsi=pd.Series(rsi,index=indexRsi)
    return(rsi)

#1

import pandas as pd
import numpy as np

jtyh = pd.read_csv('Data/Part5/003/problem29-1.csv',
                index_col='date')               
jtyh.index.name='Date'
jtyh.index = pd.to_datetime(jtyh.index,format='%Y-%m-%d')
RSI5 = rsi(jtyh.Close,5)
RSI6 = rsi(jtyh.Close,6)
RSI7 = rsi(jtyh.Close,7)
RSI8 = rsi(jtyh.Close,8)
RSI9 = rsi(jtyh.Close,9)
RSI10 = rsi(jtyh.Close,10)
RSI12 = rsi(jtyh.Close,12)
RSI_all =pd.concat([RSI5,RSI6,RSI7,RSI8,RSI9,RSI10,RSI12],1)

#2.
jtyh = pd.read_csv('Data/Part5/003/problem29-2.csv',
                index_col='date')               
jtyh.index.name='Date'
jtyh.index = pd.to_datetime(jtyh.index,format='%Y-%m-%d')

import candle
candle.candlePlot(jtyh,'Candle Plot of Bank of Communications')

RSI6 = rsi(jtyh.Close,6)
RSI30 = rsi(jtyh.Close,30)
RSI = pd.concat([RSI6,RSI30],1)
RSI.columns=['RSI6','RSI30']
RSI.plot()


signal = np.where(RSI6>90,-1,np.where(RSI6<10,1,0))
ret = (jtyh.Close-jtyh.Close.shift(1))/jtyh.Close.shift(1)
ret6 = ret[6:]
signal = pd.Series(signal,index=ret6.index)
RSI_ret = ret6[1:] * signal.shift(1)[1:]
sum(RSI_ret>0)/sum(signal!=0)


RSI_all = pd.concat([RSI6,RSI30,RSI6.shift(1),RSI30.shift(1)],1)
RSI_all = RSI_all.dropna()
RSI_all.columns = ['RSI6','RSI30','L_RSI6','L_RSI30']
signal = [1 if RSI_all.RSI6[i] > RSI_all.RSI30[i] and RSI_all.L_RSI6[i] < RSI_all.L_RSI30[i] else \
          -1 if RSI_all.RSI6[i] < RSI_all.RSI30[i] and RSI_all.L_RSI6[i] > RSI_all.L_RSI30[i] else 0 \
          for i in range(len(RSI_all))]              
ret30 = ret[30:]
signal = pd.Series(signal,index=ret30.index)
RSI_ret = ret30[1:] * signal.shift(1)[1:]
sum(RSI_ret>0)/sum(signal!=0)

#3.
RSI_all = pd.concat([RSI6,RSI30],1)[24:]
signal = np.zeros(len(RSI_all))
RSI_all.columns = ['RSI6','RSI30']

for i in range(3,len(RSI_all)):
    if RSI_all.RSI6[i-3] < RSI_all.RSI30[i-3] and \
    RSI_all.RSI6[i-2] > RSI_all.RSI30[i-2] and \
    RSI_all.RSI6[i-1] > RSI_all.RSI30[i-1] and \
    (RSI_all.RSI6[i-1] - RSI_all.RSI30[i-1]) < (RSI_all.RSI6[i-2] - RSI_all.RSI30[i-2]) and \
    (RSI_all.RSI6[i] - RSI_all.RSI30[i]) > (RSI_all.RSI6[i-1] - RSI_all.RSI30[i-1]):
        signal[i] = 1

signal = pd.Series(signal,index = RSI_all.index)
signal[signal==1]

buyDate=signal[signal==1]
ret.shift(-1)[buyDate.index]
