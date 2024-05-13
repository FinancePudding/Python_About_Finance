'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\031')
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ChinaUnicom=pd.read_csv('ChinaUnicom.csv')
ChinaUnicom.index=ChinaUnicom.iloc[:,1]
ChinaUnicom.index=pd.to_datetime(ChinaUnicom.index, format='%Y-%m-%d')
ChinaUnicom=ChinaUnicom.iloc[:,2:]

Close=ChinaUnicom.Close
High=ChinaUnicom.High
Low=ChinaUnicom.Low

upboundDC=pd.Series(0.0,index=Close.index)
downboundDC=pd.Series(0.0,index=Close.index)
midboundDC=pd.Series(0.0,index=Close.index)

for i in range(20,len(Close)):
    upboundDC[i]=max(High[(i-20):i])
    downboundDC[i]=min(Low[(i-20):i])
    midboundDC[i]=0.5*(upboundDC[i]+downboundDC[i])

upboundDC=upboundDC[20:]
downboundDC=downboundDC[20:]
midboundDC= midboundDC[20:]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close['2013'],label="Close",color='k')
plt.plot(upboundDC['2013'],label="upboundDC",color='b',linestyle='dashed')
plt.plot(midboundDC['2013'],label="midboundDC",color='r',linestyle='-.')
plt.plot(downboundDC['2013'],label="downboundDC",color='b',linestyle='dashed')
plt.title("2013年中国联通股价唐奇安通道")
plt.ylim(2.9,3.9)
plt.legend()



upDownDC=pd.DataFrame({'upboundDC':upboundDC,\
                      'downboundDC':downboundDC})
ChinaUnicom13=ChinaUnicom['2013-01-01':'2013-06-28']
upDownDC13=upDownDC['2013-01-01':'2013-06-28']


import candle
candle.candleLinePlots(candleData=ChinaUnicom13,\
        candleTitle='中国联通2013年上半年K线图及唐奇安通道',\
        Data=upDownDC13)


def upbreak(tsLine,tsRefLine):
    n=min(len(tsLine),len(tsRefLine))
    tsLine=tsLine[-n:]
    tsRefLine=tsRefLine[-n:]
    signal=pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]>tsRefLine[i],tsLine[i-1]<tsRefLine[i-1]]):
            signal[i]=1
    return(signal)

def downbreak(tsLine,tsRefLine):
    n=min(len(tsLine),len(tsRefLine))
    tsLine=tsLine[-n:]
    tsRefLine=tsRefLine[-n:]
    signal=pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]<tsRefLine[i],tsLine[i-1]>tsRefLine[i-1]]):
            signal[i]=1
    return(signal)

#DC Strategy
UpBreak=upbreak(Close[upboundDC.index[0]:],upboundDC)
DownBreak=downbreak(Close[downboundDC.index[0]:],\
          downboundDC)
BreakSig=UpBreak-DownBreak

tradeSig=BreakSig.shift(1)
ret=Close/Close.shift(1)-1
tradeRet=(ret*tradeSig).dropna()
tradeRet[tradeRet==0]=0
winRate=len(tradeRet[tradeRet>0]\
            )/len(tradeRet[tradeRet!=0])
winRate

#40日DC
upboundDC2=pd.Series(0.0,index=Close.index)
downboundDC2=pd.Series(0.0,index=Close.index)
midboundDC2=pd.Series(0.0,index=Close.index)

for i in range(40,len(Close)):
    upboundDC2[i]=max(High[(i-40):i])
    downboundDC2[i]=min(Low[(i-40):i])
    midboundDC2[i]=0.5*(upboundDC2[i]+downboundDC2[i])

upboundDC2=upboundDC2[40:]
downboundDC2=downboundDC2[40:]
midboundDC2= midboundDC2[40:]

upDownDC2=pd.DataFrame({'upboundDC':upboundDC2,\
                      'downboundDC':downboundDC2})
ChinaUnicom13=ChinaUnicom['2013-01-01':'2013-06-28']
upDownDC2=upDownDC2['2013-01-01':'2013-06-28']

import candle
candle.candleLinePlots(candleData=ChinaUnicom13,\
        candleTitle='中国联通2013年上半年K线图及40日唐奇安通道',\
        Data=upDownDC2)


UpBreak2=upbreak(Close[upboundDC2.index[0]:],upboundDC2)
DownBreak2=downbreak(Close[downboundDC2.index[0]:],downboundDC2)
BreakSig2=UpBreak2-DownBreak2
tradeSig2=BreakSig2.shift(1)
tradeRet2=(ret*tradeSig2).dropna()
tradeRet2[tradeRet2==0]=0
winRate2=len(tradeRet2[tradeRet2>0]\
         )/len(tradeRet2[tradeRet2!=0])
winRate2

#BBands
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

UnicomBBands=bbands(Close,20,2)
UnicomBBands.head()

upDownBB=UnicomBBands[['downBBand','upBBand']]
upDownBB13=upDownBB['2013-01-01':'2013-06-28']

import candle
candle.candleLinePlots(candleData=ChinaUnicom13,\
        candleTitle='中国联通2013年上半年布林带通道线',\
        Data=upDownBB13)



def CalBollRisk(tsPrice,multiplier):
    k=len(multiplier)
    overUp=[]
    belowDown=[]
    BollRisk=[]
    for i in range(k):
        BBands=bbands(tsPrice,20,multiplier[i])
        a=0
        b=0
        for j in range(len(BBands)):
            tsPrice=tsPrice[-(len(BBands)):]
            if tsPrice[j]>BBands.upBBand[j]:
                a+=1
            elif tsPrice[j]<BBands.downBBand[j]:
                b+=1
        overUp.append(a)
        belowDown.append(b)
        BollRisk.append(100*(a+b)/len(tsPrice))
    return(BollRisk)

multiplier=[1,1.65,1.96,2,2.58]
price2010=Close['2010-01-04':'2010-12-31']
CalBollRisk(price2010,multiplier)

price2011=Close['2011-01-04':'2011-12-31']
CalBollRisk(price2011,multiplier)

price2012=Close['2012-01-04':'2012-12-31']
CalBollRisk(price2012,multiplier)

price2013=Close['2013-01-04':'2013-12-31']
CalBollRisk(price2013,multiplier)


#strategy
BBands=bbands(Close,20,2)

upbreakBB1=upbreak(Close,BBands.upBBand)
downbreakBB1=downbreak(Close,BBands.downBBand)

upBBSig1=-upbreakBB1.shift(2)
downBBSig1=downbreakBB1.shift(2)

tradSignal1=upBBSig1+downBBSig1
tradSignal1[tradSignal1==0]=0

def perform(tsPrice,tsTradSig):
    ret=tsPrice/tsPrice.shift(1)-1
    tradRet=(ret*tsTradSig).dropna()
    ret=ret[-len(tradRet):]
    winRate=[len(ret[ret>0])/len(ret[ret!=0]),\
             len(tradRet[tradRet>0])/len(tradRet[tradRet!=0])]
    meanWin=[np.mean(ret[ret>0]),\
             np.mean(tradRet[tradRet>0])]
    meanLoss=[np.mean(ret[ret<0]),\
             np.mean(tradRet[tradRet<0])]
    Performance=pd.DataFrame({'winRate':winRate,'meanWin':meanWin,\
                             'meanLoss':meanLoss})
    Performance.index=['Stock','Trade']
    return(Performance)

Performance1= perform(Close,tradSignal1)
Performance1

upbreakBB2=upbreak(Close,BBands.downBBand)
downbreakBB2=downbreak(Close,BBands.upBBand)

upBBSig2=upbreakBB2.shift(2)
downBBSig2=-downbreakBB2.shift(2)
tradSignal2=upBBSig2+downBBSig2
tradSignal2[tradSignal2==0]=0

Performance2= perform(Close,tradSignal2)
Performance2
