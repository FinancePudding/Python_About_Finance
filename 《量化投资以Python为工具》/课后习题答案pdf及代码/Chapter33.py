# -*- coding: utf-8 -*-

import pandas as pd

import numpy as np

import movingAverage as ma

import matplotlib.pyplot as plt

import candle

#1.
cjzq = pd.read_csv('Data/Part5/007/problem33-1.csv',
                index_col='date')
                
cjzq.index.name='Date'

cjzq.index = pd.to_datetime(cjzq.index,format='%Y-%m-%d')

candle.candleVolume(cjzq,
    candletitle='Candle Plot of Changjiang Securities',
    bartitle='Volume of Changjiang Securities')

#2.
close = cjzq.Close

close.describe()

BreakClose = np.ceil(close)
BreakClose.name = 'BreakClose'

volume = cjzq.Volume
PrcChange = close.diff()

UpVol = volume.replace(volume[PrcChange>0],0)
UpVol[0] = 0

DownVol = volume.replace(volume[PrcChange<=0],0)
DownVol[0] = 0

def VOblock(vol):
    return([np.sum(vol[BreakClose==x]) for x in range(6,12)])
    
cumUpVol = VOblock(UpVol)
cumDownVol = VOblock(DownVol)

ALLVol = np.array([cumUpVol,cumDownVol]).transpose()

fig,ax=plt.subplots()
ax1=ax.twiny()
ax.plot(close)
ax.set_title('Cumulative volume in different price intervals')
ax.set_ylim(6,12)
ax.set_xlabel('time')

plt.setp(ax.get_xticklabels(), rotation=20,horizontalalignment='center')

ax1.barh(bottom=range(6,12),width=ALLVol[:,0],
         height=1,color='g',alpha=0.2)        
ax1.barh(bottom=range(6,12),width=ALLVol[:,1],height=1,left=ALLVol[:,0],
        color='r',alpha=0.2)
#3.       
VoMA = np.zeros(len(cjzq))
for i in range(5,len(cjzq)):
    Volume = volume[i-5:i]
    Close = close[i-5:i]
    VoMA[i] = sum(Close * Volume / sum(Volume))
VoMA = pd.Series(VoMA,index = cjzq.index).replace(0,np.nan).dropna()
VoMA.plot()

#4.
midbound = VoMA

upbound = midbound + 1.5 * pd.rolling_std(midbound,6)

lowbound = midbound - 1.5 * pd.rolling_std(midbound,6)

dat = pd.concat([close,upbound,lowbound],1).dropna()

dat.columns = ['price','upbound','lowbound']

asset = 2000 * np.ones(len(dat))

cash = 2000 * np.ones(len(dat))

share = np.zeros(len(dat))

for i in range(1,len(dat)):
    cash[i]=cash[i-1]+share[i-1]*dat.price[i]
    asset[i]=cash[i]
    if dat.price[i-1]< dat.upbound[i-1]:
        share[i]=100
        cash[i]=cash[i]-100*dat.price[i]
    elif dat.price[i-1]>dat.lowbound[i-1]:
        share[i]=-100
        cash[i]=cash[i]+100*dat.price[i]