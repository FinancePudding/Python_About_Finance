'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\033')
'''

import pandas as pd
import numpy as np
CJSecurities=pd.read_csv('CJSecurities.csv',index_col='Date')
CJSecurities=CJSecurities.iloc[:,1:]
CJSecurities.index=pd.to_datetime(CJSecurities.index)
CJSecurities.head()

from candle import candleVolume
CJSecurities1=CJSecurities['2015-04-01':'2015-04-30']
candleVolume(CJSecurities1,candletitle='长江证券2015年4月份蜡烛图',\
             bartitle='长江证券2015年4月份日成交量')

CJSecurities2=CJSecurities['2015-01-15':'2015-02-15']
candleVolume(CJSecurities2,candletitle='长江证券2015年1月和2月份蜡烛图',\
            bartitle='长江证券2015年1月和2月份日成交量')

CJSecurities3=CJSecurities['2015-03-01':'2015-03-31']
candleVolume(CJSecurities3,candletitle='长江证券2015年3月份蜡烛图',\
             bartitle='长江证券2015年3月份日成交量')

CJSecurities4=CJSecurities['2014-01-02':'2014-03-31']
candleVolume(CJSecurities4,candletitle='长江证券2014年前3个月份蜡烛图',\
            bartitle='长江证券2014年前3个月份日成交量')


close=CJSecurities.Close
close.describe()
BreakClose=np.ceil(close/2)*2
BreakClose.name='BreakClose'
pd.DataFrame({'BreakClose':BreakClose,\
            'Close':close}).head(n=2)

volume=CJSecurities.Volume

PrcChange=close.diff()

UpVol=volume.replace(volume[PrcChange>0],0)
UpVol[0]=0
DownVol=volume.replace(volume[PrcChange<=0],0)
DownVol[0]=0

def VOblock(vol):
    return([np.sum(vol[BreakClose==x]) for x in range(6,22,2)])

cumUpVol=VOblock(UpVol)
cumDownVol=VOblock(DownVol)
ALLVol=np.array([cumUpVol,cumDownVol]).transpose()

import matplotlib.pyplot as plt
fig,ax=plt.subplots()
ax1=ax.twiny()
ax.plot(close)
ax.set_title('不同价格区间的累积成交量图')
ax.set_ylim(4,20)
ax.set_xlabel('时间')
plt.setp(ax.get_xticklabels(), rotation=20,horizontalalignment='center')
ax1.barh(bottom=range(4,20,2),width=ALLVol[:,0],\
         height=2,color='g',alpha=0.2)
ax1.barh(bottom=range(4,20,2),width=ALLVol[:,1],height=2,left=ALLVol[:,0],\
        color='r',alpha=0.2)
plt.show()

volume=CJSecurities.Volume
VolSMA5=pd.rolling_apply(volume,5,np.mean).dropna()
VolSMA10=pd.rolling_apply(volume,10,np.mean).dropna()
VolSMA=((VolSMA5+VolSMA10)/2).dropna()
VolSMA.head(n=3)

VolSignal=(volume[-len(VolSMA):]>VolSMA)*1
VolSignal[VolSignal==0]=-1
VolSignal.head()

close=CJSecurities.Close
PrcSMA5=pd.rolling_apply(close,5,np.mean).dropna()
PrcSMA20=pd.rolling_apply(close,20,np.mean).dropna()

def upbreak(Line,RefLine):
    signal=np.all([Line>RefLine,Line.shift(1)<RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))
def downbreak(Line,RefLine):
    signal=np.all([Line<RefLine,Line.shift(1)>RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))

UpSMA=upbreak(PrcSMA5[-len(PrcSMA20):],PrcSMA20)*1
DownSMA=downbreak(PrcSMA5[-len(PrcSMA20):],PrcSMA20)*1
SMAsignal=UpSMA-DownSMA
VolSignal=VolSignal[-len(SMAsignal):]
signal=VolSignal+SMAsignal
signal.describe()

trade=signal.replace([2,-2,1,-1,0],[1,-1,0,0,0])
trade=trade.shift(1)[1:]
trade.head()

ret=((close-close.shift(1))/close.shift(1))['2014-01-31':]
ret.name='stockRet'
tradeRet=trade*ret
tradeRet.name='tradeRet'
winRate=len(tradeRet[tradeRet>0])/len(tradeRet[tradeRet!=0])
winRate

(1+ret).cumprod().plot(label='stockRet')
(1+tradeRet).cumprod().plot(label='tradeRet')
plt.legend()


def Hold(signal):
    hold=np.zeros(len(signal))
    for index in range(1,len(hold)):
        if hold[index-1]==0 and signal[index]==1:
            hold[index]=1
        elif hold[index-1]==1 and signal[index]==1:
            hold[index]=1
        elif hold[index-1]==1 and signal[index]==0:
            hold[index]=1
    return(pd.Series(hold,index=signal.index))

hold=Hold(trade)

def TradeSim(price,hold):
    position=pd.Series(np.zeros(len(price)),index=price.index)
    position[hold.index]=hold.values
    cash=20000*np.ones(len(price))
    for t in range(1,len(price)):
        if position[t-1]==0 and position[t]>0:
            cash[t]=cash[t-1]-price[t]*1000
        if position[t-1]>=1 and position[t]==0:
            cash[t]=cash[t-1]+price[t]*1000
        if position[t-1]==position[t]:
            cash[t]=cash[t-1]
    asset=cash+price*position*1000
    asset.name='asset'
    account=pd.DataFrame({'asset':asset,'cash':cash,'position':position})
    return(account)

TradeAccount=TradeSim(close,hold)
TradeAccount.tail()
TradeAccount.plot(subplots=True,\
        title='成交量与均线策略交易账户')