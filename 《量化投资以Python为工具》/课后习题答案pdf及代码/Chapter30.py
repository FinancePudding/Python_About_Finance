# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import movingAverage as ma


#1.
dow = pd.read_csv('Data/Part5/004/problem30-1.csv',
                index_col='date')               
dow.index.name='Date'
dow.index = pd.to_datetime(dow.index,format='%Y-%m-%d')

sma = ma.smaCal(dow.Close,30)
wma = ma.wmaCal(dow.Close,[(i+1)/465 for i in range(30)])
ema = ma.ewmaCal(dow.Close,30,0.8)

maValues = pd.concat([sma,wma,ema],1).replace(0,np.nan).dropna()
maValues.columns = ['sma','wma','ema']
maValues.plot()



#2.
zgyh = pd.read_csv('Data/Part5/004/problem30-2.csv',
                index_col='date')
                
zgyh.index.name='Date'

zgyh.index = pd.to_datetime(zgyh.index,format='%Y-%m-%d')

import matplotlib.pyplot as plt
mom14 = (zgyh.Close-zgyh.Close.shift(14))/zgyh.Close.shift(14)

ma14 = ma.smaCal(zgyh.Close,14)

data = pd.concat([zgyh.Close,mom14,ma14],1).dropna()

data.columns = ['Close','Mom','SMA']

axis1 = plt.subplot()
plot1, = axis1.plot(data.index,data.Close,'-r',label='Close')
plot2, = axis1.plot(data.index,data.SMA,'-g',label='SMA')
axis2 = axis1.twinx()
plot3, = axis2.plot(data.index,data.Mom,'-b',label='Mom')
plt.legend(handles=[plot1,plot2,plot3])

ret = (zgyh.Close-zgyh.Close.shift(1))/zgyh.Close.shift(1)
signal = np.all([data.Close > data.SMA, data.Mom>0],0)
signal = pd.Series(signal,index = ret[14:].index)
ret = ret[15:] * signal.shift(1)[1:]
ret.sum()

#3.
aapl = pd.read_csv('Data/Part5/004/problem30-3.csv',
                index_col='date')
                
aapl.index.name='Date'

aapl.index = pd.to_datetime(aapl.index,format='%Y-%m-%d')

import candle
candle.candleLinePlots(aapl['2014-01':'2014-02'],
    candleTitle='Candle Plot of AAPL',
    Data=aapl.Close['2014-01':'2014-02'])

                       
aapl1 = aapl[:'2014-05']
#因为苹果发放了股利，为了价格的一致性，我们选取了Adjusted Price，即复权过的价格
dif = ma.ewmaCal(aapl1.Adjusted,12,2/13)-ma.ewmaCal(aapl1.Adjusted,26,2/27)
dif = dif[25:]
dea = ma.ewmaCal(dif,9,2/10)
dea = dea[8:]
dif = dif[8:]

macd = dif -dea

plt.subplot(211)
plt.plot(dif[12:],label="DIF",color='k')
plt.plot(dea[12:], label="DEA",color='b',linestyle='dashed')
plt.title("DIF and DEA")
plt.legend()
plt.subplot(212)
plt.bar(left=macd[12:].index,height=macd[12:],
       label='MACD',color='r')
plt.legend()


price = aapl1.Adjusted
dat = pd.concat([price,dea,dif],1).dropna()
dat.columns = ['price','dea','dif']
asset = 100000 * np.ones(len(dat))
cash = 100000 * np.ones(len(dat))
share = np.zeros(len(dat))
for i in range(1,len(dat)):
    cash[i]=cash[i-1]+share[i-1]*dat.price[i]
    asset[i]=cash[i]
    if dat.dif[i] > dat.dea[i] >0 and dat.dif[i-1] < dat.dea[i-1]:
        share[i]=100
        cash[i]=cash[i]-100*dat.price[i]
    elif dat.dif[i] < dat.dea[i] < 0 and dat.dif[i-1] > dat.dea[i-1]:
        share[i]=-100 #short
        cash[i]=cash[i]+100*dat.price[i]        
asset[-5:]

#4.
SMA6 = ma.smaCal(aapl.Close,6)
BIAS6 = (aapl.Close-SMA6)/SMA6*100
EMA9 = ma.ewmaCal(aapl.Close,9)
SMA38 = ma.smaCal(aapl.Close,38)
BIAS = (EMA9 - SMA38)/SMA38

