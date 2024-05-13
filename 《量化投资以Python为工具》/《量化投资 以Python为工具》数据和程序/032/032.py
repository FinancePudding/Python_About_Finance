'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\032')
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

GSPC=pd.read_csv('GSPC.csv',index_col='Date')
GSPC=GSPC.iloc[:,1:]
GSPC.index=pd.to_datetime(GSPC.index)
GSPC.head()

close=GSPC.Close
high=GSPC.High
low=GSPC.Low


date=close.index.to_series()
ndate=len(date)

periodHigh=pd.Series(np.zeros(ndate-8),\
                  index=date.index[8:])
periodLow=pd.Series(np.zeros(ndate-8),\
                    index=date.index[8:])
RSV=pd.Series(np.zeros(ndate-8),\
               index=date.index[8:])

for j in range(8,ndate):
    period=date[j-8:j+1]
    i=date[j]
    periodHigh[i]=high[period].max()
    periodLow[i]=low[period].min()
    RSV[i]=100*(close[i]-periodLow[i])\
           /(periodHigh[i]-periodLow[i])
    periodHigh.name='periodHigh'
    periodLow.name='periodLow'
    RSV.name='RSV'

periodHigh.head(3)
periodLow.head(3)
RSV.head()
RSV.describe()

close1=close['2015']
RSV1=RSV['2015']
Cl_RSV=pd.DataFrame([close1,RSV1]).transpose()
Cl_RSV.plot(subplots=True,
             title='未成熟随机指标RSV')

GSPC2015=GSPC['2015']

import candle
candle.candlePlot(GSPC2015,\
                '标普500指数2015年日K线图')

RSV1=pd.Series([50,50],index=date[6:8]).append(RSV)
RSV1.name='RSV'
RSV1.head()

KValue=pd.Series(0.0,index=RSV1.index)

KValue[0]=50
for i in range(1,len(RSV1)):
    KValue[i]=2/3*KValue[i-1]+RSV1[i]/3
KValue.name='KValue'
KValue.head()

DValue=pd.Series(0.0,index=RSV1.index)
DValue[0]=50
for i in range(1,len(RSV1)):
    DValue[i]=2/3*DValue[i-1]+KValue[i]/3

KValue=KValue[1:]
DValue.name='DValue'
DValue=DValue[1:]
DValue.head()

plt.subplot(211)
plt.title('2015年标准普尔500的收盘价')
plt.plot(close['2015'])
plt.subplot(212)
plt.title('2015年标准普尔500的RSV与KD线')
plt.plot(RSV['2015'])
plt.plot(KValue['2015'],linestyle='dashed')
plt.plot(DValue['2015'],linestyle='-.')
plt.legend(loc='upper left')

JValue=3*KValue-2*DValue
JValue.name='JValue'
JValue.head()

plt.subplot(211)
plt.title('2015年标准普尔500的收盘价')
plt.plot(close['2015'])
plt.subplot(212)
plt.title('2015年标准普尔500的RSV与KD线')
plt.plot(RSV['2015'])
plt.plot(KValue['2015'],linestyle='dashed')
plt.plot(DValue['2015'],linestyle='-.')
plt.plot(JValue['2015'],linestyle='--')
plt.legend(loc='upper left')


KSignal=KValue.apply(lambda x:\
                    -1 if x>85 else 1 if x<20 else 0)

DSignal=DValue.apply(lambda x: \
                 -1 if x>80 else 1 if x<20 else 0)
KDSignal=KSignal+DSignal
KDSignal.name='KDSignal'

KDSignal[KDSignal>=1]==1
KDSignal[KDSignal<=-1]==-1
KDSignal.head(n=3)
KDSignal[KDSignal==1].head(n=3)

def trade(signal,price):
    ret=((price-price.shift(1))/price.shift\
         (1))[1:]
    ret.name='ret'
    signal=signal.shift(1)[1:]
    tradeRet=ret*signal+0
    tradeRet.name='tradeRet'
    Returns=pd.merge(pd.DataFrame(ret),\
                     pd.DataFrame(tradeRet),
                     left_index=True,\
                     right_index=True).dropna()
    return(Returns)

KDtrade=trade(KDSignal,close)
KDtrade.rename(columns={'ret':'Ret',\
              'tradeRet':'KDtradeRet'},\
               inplace=True)
KDtrade.head()

import ffn
def backtest(ret,tradeRet):
    def performance(x):
        winpct=len(x[x>0])/len(x[x!=0])
        annRet=(1+x).cumprod()[-1]**(245/len(x))-1
        sharpe=ffn.calc_risk_return_ratio(x)
        maxDD=ffn.calc_max_drawdown((1+x).cumprod())
        perfo=pd.Series([winpct,annRet,sharpe,maxDD],\
        index=['win rate','annualized return',\
        'sharpe ratio','maximum drawdown'])
        return(perfo)
    BuyAndHold=performance(ret)
    Trade=performance(tradeRet)
    return(pd.DataFrame({ret.name:BuyAndHold,\
           tradeRet.name:Trade}))

backtest(KDtrade.Ret,KDtrade.KDtradeRet)

cumRets1=(1+KDtrade).cumprod()
plt.plot(cumRets1.Ret,label='Ret')
plt.plot(cumRets1.KDtradeRet,'--',\
          label='KDtradeRet')
plt.title('KD指标交易策略绩效表现')
plt.legend()

backtest(KDtrade.Ret[:'2014-10-10'],\
          KDtrade.KDtradeRet[:'2014-10-10'])

cumRets2=(1+KDtrade[:'2014-10-10']).cumprod()
plt.plot(cumRets2.Ret,\
          label='''Ret[:'2014-10-10']''')
plt.plot(cumRets2.KDtradeRet,'--',\
          label='''KDtradeRet[:'2014-10-10']''')
plt.title('KD指标交易策略10月10日之前绩效表现')
plt.legend(loc='upper left')


JSignal=JValue.apply(lambda x:\
         -1 if x>100 else 1 if x<0 else 0)


KDJSignal=KSignal+DSignal+JSignal
KDJSignal=KDJSignal.apply(lambda x:\
          1 if x>=2 else -1 if x<=-2 else 0)

KDJtrade=trade(KDJSignal,close)
KDJtrade.rename(columns={'ret':'Ret',\
             'tradeRet':'KDJtradeRet'},\
             inplace=True)
backtest(KDJtrade.Ret,KDJtrade.KDJtradeRet)

KDJCumRet=(1+KDJtrade).cumprod()
plt.plot(KDJCumRet.Ret,label='Ret')
plt.plot(KDJCumRet.KDJtradeRet,'--',\
          label='KDJtradeRet')
plt.title('KDJ指标交易策略绩效表现')
plt.legend(loc='upper left')

backtest(KDJtrade.Ret[:'2014-10-10'],\
             KDJtrade.KDJtradeRet[:'2014-10-10'])

def upbreak(Line,RefLine):
    signal=np.all([Line>RefLine,\
                   Line.shift(1)<RefLine.shift(1)],\
                   axis=0)
    return(pd.Series(signal[1:],\
                     index=Line.index[1:]))

KDupbreak=upbreak(KValue,DValue)*1
KDupbreak[KDupbreak==1].head()

def downbreak(Line,RefLine):
    signal=np.all([Line<RefLine,\
                   Line.shift(1)>RefLine.shift(1)],\
                   axis=0)
    return(pd.Series(signal[1:],\
           index=Line.index[1:]))

KDdownbreak=downbreak(KValue,DValue)*1
KDdownbreak[KDdownbreak==1].head()

close=close['2014-01-14':]
difclose=close.diff()

prctrend=2*(difclose[1:]>=0)-1
prctrend.head()

KDupSig=(KDupbreak[1:]+prctrend)==2
KDupSig.head(n=3)

KDdownSig=pd.Series(np.all([KDdownbreak[1:]==1,prctrend==-1],\
                    axis=0),\
                  index=prctrend.index)

breakSig=KDupSig*1+KDdownSig*-1
breakSig.name='breakSig'
breakSig.head()

KDbreak=trade(breakSig,close)
KDbreak.rename(columns={'ret':'Ret',\
              'tradeRet':'KDbreakRet'},\
              inplace=True)
KDbreak.head()

backtest(KDbreak.Ret,KDbreak.KDbreakRet)

KDbreakRet=(1+KDbreak).cumprod()
plt.plot(KDbreakRet.Ret,label='Ret')
plt.plot(KDbreakRet.KDbreakRet,'--',\
          label='KDbreakRet')
plt.title('KD"金叉"与"死叉"交易策略绩效表现')
plt.legend(loc='upper left')