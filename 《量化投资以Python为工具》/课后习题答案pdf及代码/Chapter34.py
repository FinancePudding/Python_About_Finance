# -*- coding: utf-8 -*-

import pandas as pd

import numpy as np
#1.
she = pd.read_csv('Data/Part5/008/problem34-1.csv',
                index_col='date')              
she.index.name='Date'
she.index = pd.to_datetime(she.index,format='%Y-%m-%d')

MendOBV = (she.Volume * ((she.Close-she.Low) - (she.High-she.Close))\
        /(she.High - she.Low)).cumsum().dropna()       
signal = pd.Series(np.where(MendOBV.diff()>0 , 1, -1),index = MendOBV.index)[1:]
ret = (she.Close - she.Close.shift(1))/she.Close.shift(1)
OBVret = ret[2:] * signal.shift(1)[1:]

sum(OBVret>0)/len(signal)

dat = pd.concat([signal,she.Close],1).dropna()
dat.columns = ['signal','price']

asset = 10000 * np.ones(len(dat))
cash = 10000 * np.ones(len(dat))
share = np.zeros(len(dat))
for i in range(1,len(dat)):
    cash[i]=cash[i-1]+share[i-1]*dat.price[i]
    asset[i]=cash[i]
    if dat.signal[i-1] == 1:
        share[i]=100
        cash[i]=cash[i]-100*dat.price[i]
    elif dat.signal[i-1] == -1:
        share[i]=-100
        cash[i]=cash[i]+100*dat.price[i]
#2.       
difClose = she.Close.diff()

difClose[0] = 0

volume = she.Volume

volume = volume.replace(0, np.nan).dropna()

difClose = difClose[volume.index]

OBV=(((difClose>=0)*2-1) * she.Volume).cumsum()

dat = pd.concat([OBV,she.Close],1).dropna()

dat.columns = ['OBV','price']

asset = 10000 * np.ones(len(dat))

cash = 10000 * np.ones(len(dat))

share = np.zeros(len(dat))

for i in range(2,len(dat)):
    cash[i]=cash[i-1]+share[i-1]*dat.price[i]
    asset[i]=cash[i]
    if dat.OBV[i-2] < 0 and dat.OBV[i-1] > 0:
        share[i]=100
        cash[i]=cash[i]-100*dat.price[i]
    elif dat.OBV[i-2] > 0 and dat.OBV[i-1] < 0:
        share[i]=-100
        cash[i]=cash[i]+100*dat.price[i]

#3.
wanke = pd.read_csv('Data/Part5/008/problem34-3.csv',
                index_col='date')
                
wanke.index.name='Date'

wanke.index = pd.to_datetime(wanke.index,format='%Y-%m-%d')

difClose = wanke.Close.diff()

difClose[0] = 0

volume = wanke.Volume

volume = volume.replace(0, np.nan).dropna()

difClose = difClose[volume.index]

OBV=(((difClose>=0)*2-1) * wanke.Volume).cumsum()

smOBV = pd.rolling_mean(OBV,12)