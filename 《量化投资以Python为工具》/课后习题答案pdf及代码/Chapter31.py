# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import candle

def bbands(tsPrice,period=20,times=2):
    upBBand=pd.Series(0.0,index=tsPrice.index)
    midBBand=pd.Series(0.0,index=tsPrice.index)
    downBBand=pd.Series(0.0,index=tsPrice.index)
    sigma=pd.Series(0.0,index=tsPrice.index)
    for i in range(period-1,len(tsPrice)):
        midBBand[i]=np.nanmean(tsPrice[i-(period-1):(i+1)])
        sigma[i]=np.nanstd(tsPrice[i-(period-1):(i+1)])
        upBBand[i]=midBBand[i]+times*sigma[i]
        downBBand[i]=midBBand[i]-times*sigma[i]
    BBands=pd.DataFrame({'upBBand':upBBand[(period-1):],\
                         'midBBand':midBBand[(period-1):],\
                         'downBBand':downBBand[(period-1):],\
                         'sigma':sigma[(period-1):]})
    return(BBands)

#1.
GSPC = pd.read_csv('Data/Part5/005/problem31-1.csv',
                index_col='date')
                
GSPC.index.name='Date'

GSPC.index = pd.to_datetime(GSPC.index,format='%Y-%m-%d')

GSPC1 = GSPC[:'2014-02']


candle.candleLinePlots(GSPC1,
  candleTitle='Candle Plot of SPY500',
  Data=GSPC1.Close)

candle.candleLinePlots(GSPC1,candleTitle='Candle Plot of SPY500',
                       Data=bbands(GSPC1.Close)[['downBBand','upBBand']])
                       
upbound = pd.rolling_max(GSPC.High,10)
lowbound = pd.rolling_min(GSPC.Low,10)
midbound = (upbound+lowbound)/2
bounds = pd.concat([upbound,lowbound,midbound],1)
bounds.columns=['upbound','lowbound','midbound']
bounds.dropna().plot()

std = pd.rolling_std(GSPC.Close,10)
midbound = pd.rolling_mean(GSPC.Close,10)
upbound = midbound + 1.5 * std
lowbound = midbound - 1.5 * std
bounds = pd.concat([upbound,lowbound,midbound],1)
bounds.columns=['upbound','lowbound','midbound']
bounds.dropna().plot()

#2.
bounds = bbands(GSPC.Close)
bvalue = (GSPC.Close - bounds.downBBand)/(bounds.upBBand-bounds.downBBand)
bvalue.plot()

bvalue = bvalue.dropna()
dat = pd.concat([GSPC.Close,bvalue],1).dropna()
dat.columns = ['price','bvalue']
asset = 100000 * np.ones(len(dat))
cash = 100000 * np.ones(len(dat))
share = np.zeros(len(dat))

for i in range(1,len(dat)):
    cash[i]=cash[i-1]+share[i-1]*dat.price[i]
    asset[i]=cash[i]
    if dat.bvalue[i-1]<0:
        share[i]=100
        cash[i]=cash[i]-100*dat.price[i]
    elif dat.bvalue[i-1]>0:
        share[i]=-100
        cash[i]=cash[i]+100*dat.price[i]
#3.      
BW = (bounds.upBBand - bounds.downBBand)/bounds.midBBand
BW.describe()

#4.
midbound = (pd.rolling_mean(GSPC.Close,3) + pd.rolling_mean(GSPC.Close,6)\
           + pd.rolling_mean(GSPC.Close,12) + pd.rolling_mean(GSPC.Close,24))/4

std = pd.rolling_std(midbound,11)

upbound = midbound + 6 * std
lowbound = midbound - 6 * std
bounds = pd.concat([upbound,lowbound,midbound],1)
bounds.columns=['upbound','lowbound','midbound']
bounds.dropna().plot()