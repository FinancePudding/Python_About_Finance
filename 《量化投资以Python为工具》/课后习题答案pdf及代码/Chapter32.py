# -*- coding: utf-8 -*-

import pandas as pd

import numpy as np

import movingAverage as ma

import matplotlib.pyplot as plt

#2.
GSPC = pd.read_csv('Data/Part5/006/problem32-2.csv',
                index_col='date')
                
GSPC.index.name='Date'

GSPC.index = pd.to_datetime(GSPC.index,format='%Y-%m-%d')

minValue = GSPC.Low.rolling(9).min()

maxValue = GSPC.High.rolling(9).max()

RSV = (GSPC.Close - minValue)/(maxValue - minValue) * 100
RSV = RSV.dropna()

K = ma.ewmaCal(RSV,2,1/3)[1:]
D = ma.ewmaCal(K,2,1/3)[1:]
J = 3*K - 2*D
J = J.dropna()

KDJ = pd.concat([K,D,J],1).dropna()
KDJ.columns = ['K','D','J']

signal1 = [1 if KDJ.K[i] < 20 else -1 if KDJ.K[i] > 80 else 0 for i in range(len(KDJ))]
signal2 = [1 if KDJ.D[i] < 20 else -1 if KDJ.D[i] > 80 else 0 for i in range(len(KDJ))]
signal3 = [1 if KDJ.J[i] < 0 else -1 if KDJ.J[i] > 100 else 0 for i in range(len(KDJ))]

signal = np.array(signal1) + np.array(signal2) + np.array(signal3)         
signal = pd.Series(signal, index = KDJ.index)

ret = (GSPC.Close - GSPC.Close.shift(1))/GSPC.Close.shift(1)
KDJRet = ret * signal.shift(1)
KDJRet = KDJRet.dropna()
sum(KDJRet>0)/sum(KDJRet!=0)

#3.
minValue = GSPC.Low.rolling(14).min()
maxValue = GSPC.High.rolling(14).max()

WR = (maxValue - GSPC.Close) / (maxValue - minValue) * 100

WR = WR.dropna()

signal = [1 if WR[i]>80 else -1 if WR[i]<20 else 0 for i in range(len(WR))]

signal = pd.Series(signal,index = WR.index)

WRRet = ret * signal.shift(1)

WRRet = WRRet.dropna()

sum(WRRet>0)/sum(signal!=0)