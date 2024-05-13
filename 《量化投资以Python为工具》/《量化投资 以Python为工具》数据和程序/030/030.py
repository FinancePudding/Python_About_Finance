'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\030')
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
TsingTao=pd.read_csv('TsingTao.csv')
TsingTao.index=TsingTao.iloc[:,1]
TsingTao.index=pd.to_datetime(TsingTao.index, format='%Y-%m-%d')
TsingTao=TsingTao.iloc[:,2:]
TsingTao.head(n=3)

Close=TsingTao.Close


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close,'k')
plt.xlabel('date')
plt.ylabel('Close')
plt.title('2014年青岛啤酒股票收盘价时序图')


Sma5=pd.Series(0.0,index=Close.index)

for i in range(4,len(Close)):
    Sma5[i]=np.mean(Close[(i-4):(i+1)])

Sma5.tail()


plt.plot(Close[4:],label="Close",color='g')
plt.plot(Sma5[4:],label="Sma5",color='r',linestyle='dashed')
plt.title("青岛啤酒股票价格图")
plt.ylim(35,50)
plt.legend()

def smaCal(tsPrice,k):
    import pandas as pd
    Sma=pd.Series(0.0,index=tsPrice.index)
    for i in range(k-1,len(Close)):
        Sma[i]=sum(Close[(i-k+1):(i+1)])/k
    return(Sma)

sma5=smaCal(Close ,5)    
sma5.tail()
    
b=np.array([1,2,3,4,5])
w=b/sum(b)
w

m1Close=Close[0:5]
wec=w*m1Close
sum(wec)


Wma5=pd.Series(0.0,index=Close.index)
for i in range(4,len(Close)):
    Wma5[i]=sum(w*Close[(i-4):(i+1)])
Wma5[2:7]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close[4:],label="Close",color='g')
plt.plot(Wma5[4:],label="Wma5",color='r',linestyle='dashed')
plt.title("青岛啤酒收盘价加权移动平均线")
plt.ylim(35,50)
plt.legend()

def wmaCal(tsPrice,weight):
   import pandas as pd
   import numpy as np
   k=len(weight)
   arrWeight=np.array(weight)
   Wma=pd.Series(0.0,index=tsPrice.index)
   for i in range(k-1,len(tsPrice.index)):
       Wma[i]=sum(arrWeight*tsPrice[(i-k+1):(i+1)])
   return(Wma)

wma5=wmaCal(Close,w)   
wma5.head()
   
wma5=wmaCal(Close,[0.1,0.15,0.2,0.25,0.3])
wma5.tail()

Ema5_number1=np.mean(Close[0:5])
Ema5_number2=0.2* Close[5]+(1-0.2)*Ema5_number1
Ema5=pd.Series(0.0,index=Close.index)
Ema5[4]=Ema5_number1
Ema5[5]=Ema5_number2

for i in range(6,len(Close)):
    expo=np.array(sorted(range(i-4),reverse=True))
    w=(1-0.2)**expo
    Ema5[i]=sum(0.2*w*Close[5:(i+1)])+Ema5_number1*0.2**(i-5)

Ema5.tail()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close[4:],label="Close",color='k')
plt.plot(Ema5[4:],label="Ema5",\
         color='g',linestyle='-.')
plt.title("青岛啤酒收盘价指数移动平均线")
plt.ylim(35,50)
plt.legend()


def ewmaCal(tsprice,period=5,exponential=0.2):
   import pandas as pd
   import numpy as np
   Ewma=pd.Series(0.0,index=tsprice.index)
   Ewma[period-1]=np.mean(tsprice[:period])
   for i in range(period,len(tsprice)):
       Ewma[i]=exponential*tsprice[i]+(1-exponential)*Ewma[period-1]
   return(Ewma)

Ewma=ewmaCal(Close,5,0.2)
Ewma.head()

import movingAverage as ma
Ewma10=ma.ewmaCal(Close,10,0.2)
Ewma10.tail(n=3)

#ChinaBank
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import movingAverage as ma
ChinaBank=pd.read_csv('ChinaBank.csv')
ChinaBank.index=ChinaBank.iloc[:,1]
ChinaBank.index=pd.to_datetime(ChinaBank.index, format='%Y-%m-%d')
ChinaBank=ChinaBank.iloc[:,2:]

CBClose=ChinaBank.Close
CBClose.describe()

Close15=CBClose['2015']

Sma10=ma.smaCal(Close15,10)
Sma10.tail(n=3)

weight=np.array(range(1,11))/sum(range(1,11))
Wma10=ma.wmaCal(Close15,weight)
Wma10.tail(n=3)

expo= 2/(len(Close15)+1)
Ema10=ma.ewmaCal(Close15,10,expo)
Ema10.tail(n=3)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close15[10:],label="Close",color='k')
plt.plot(Sma10[10:],label="Sma10",color='r',linestyle='dashed')
plt.plot(Wma10[10:],label="Wma10",color='b',linestyle=':')
plt.plot(Ema10[10:],label="Ema10",color='G',linestyle='-.')
plt.title("中国银行价格均线")
plt.ylim(3.5,5.5)
plt.legend()

Sma5=ma.smaCal(Close15,5)
Sma30=ma.smaCal(Close15,30)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close15[30:],label="Close",color='k')
plt.plot(Sma5[30:],label="Sma5",color='b',linestyle='dashed')
plt.plot(Sma30[30:],label="Sma30",color='r',linestyle=':')
plt.title("中国银行股票价格的长短期均线")
plt.ylim(3.5,5.5)
plt.legend()

#trading-sma10 and close
CBSma10=ma.smaCal(CBClose,10)

SmaSignal=pd.Series(0,index=CBClose.index)
for i in range(10,len(CBClose)):
    if all([CBClose[i]>CBSma10[i],CBClose[i-1]<CBSma10[i-1]]):
        SmaSignal[i]=1;
    elif all([CBClose[i]<CBSma10[i],CBClose[i-1]>CBSma10[i-1]]):
         SmaSignal[i]=-1;



SmaTrade=SmaSignal.shift(1).dropna()
SmaTrade.head(n=3)

SmaBuy=SmaTrade[SmaTrade==1]
SmaBuy.head(n=3)

SmaSell=SmaTrade[SmaTrade==-1]
SmaSell.head(n=3)

CBRet=CBClose/CBClose.shift(1)-1
SmaRet=(CBRet*SmaTrade).dropna()

cumStock=np.cumprod(1+CBRet[SmaRet.index[0]:])-1
cumTrade=np.cumprod(1+SmaRet)-1
cumdata=pd.DataFrame({'cumTrade':cumTrade,\
                     'cumStock':cumStock})
cumdata.iloc[-6:,:]

plt.plot(cumStock,label="cumStock",color='k')
plt.plot(cumTrade,label="cumTrade",color='r',linestyle=':')
plt.title("股票本身与均线交易的累积收益率")
plt.legend()

SmaRet[SmaRet==(-0)]=0
smaWinrate=len(SmaRet[SmaRet>0])/len(SmaRet[SmaRet!=0])
smaWinrate

#short  and  long
Ssma5=ma.smaCal(CBClose,5);
Lsma30=ma.smaCal(CBClose,30);
SLSignal=pd.Series(0,index=Lsma30.index)
for i in range(1,len(Lsma30)):
    if all([Ssma5[i]>Lsma30[i],Ssma5[i-1]<Lsma30[i-1]]):
        SLSignal[i]=1
    elif all([Ssma5[i]<Lsma30[i],Ssma5[i-1]>Lsma30[i-1]]):
         SLSignal[i]=-1

SLSignal[SLSignal==1]
SLSignal[SLSignal==-1]

SLTrade=SLSignal.shift(1)

Long=pd.Series(0,index=Lsma30.index)
Long[SLTrade==1]=1
CBRet=CBClose/CBClose.shift(1)-1
LongRet=(Long*CBRet).dropna()
winLrate=len(LongRet[LongRet>0])/len(LongRet[LongRet!= 0] )
winLrate

Short= pd.Series(0,index=Lsma30.index)
Short[SLTrade==-1]=-1
ShortRet=(Short*CBRet).dropna()
winSrate=len(ShortRet[ShortRet>0])/len(ShortRet[ShortRet!=0])
winSrate

SLtradeRet=(SLTrade*CBRet).dropna()
winRate= len(SLtradeRet[ SLtradeRet>0])/len(\
         SLtradeRet[SLtradeRet!=0])
winRate

cumLong=np.cumprod(1+LongRet)-1
cumShort=np.cumprod(1+ShortRet)-1
cumSLtrade=np.cumprod(1+SLtradeRet)-1

plt.rcParams['axes.unicode_minus'] = False
plt.plot(cumSLtrade,label="cumSLtrade",color='k')
plt.plot(cumLong, label="cumStock",\
         color='b',linestyle='dashed')
plt.plot(cumShort,label="cumTrade",\
         color='r',linestyle=':')
plt.title("长短期均线交易累计收益率")
plt.legend(loc='best')

#MACD
DIF=ma.ewmaCal(CBClose,12,2/(1+12))\
       -ma.ewmaCal(CBClose,26,2/(1+26))
DIF.tail(n=3)

DEA=ma.ewmaCal(DIF,9,2/(1+9))
DEA.tail()

MACD=DIF-DEA
MACD.tail(n=3)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.subplot(211)
plt.plot(DIF['2015'],\
      label="DIF",color='k')
plt.plot(DEA['2015'], label="DEA",\
        color='b',linestyle='dashed')
plt.title("信号线DIF与DEA")
plt.legend()
plt.subplot(212)
plt.bar(left=MACD['2015'].index,\
        height=MACD['2015'],\
        label='MACD',color='r')
plt.legend()

macddata=pd.DataFrame()
macddata['DIF']= DIF['2015']
macddata['DEA']= DEA['2015']
macddata['MACD']= MACD['2015']

import candle
candle.candleLinePlots(ChinaBank['2015'],\
              candleTitle='中国银行2015年日K线图',\
              splitFigures=True,Data=macddata,\
              ylabel='MACD')


macdSignal=pd.Series(0,index=DIF.index)
for i in range(1,len(DIF)):
    if all([DIF[i]>DEA[i]>0.0,DIF[i-1]<DEA[i-1]]):
        macdSignal[i]=1
    elif all([DIF[i]<DEA[i]<0.0,DIF[i-1]>DEA[i-1]]):
        macdSignal[i]=-1
macdSignal.tail()

macdTrade=macdSignal.shift(1)

CBRet=CBClose/CBClose.shift(1)-1
macdRet=(CBRet*macdTrade).dropna()
macdRet[macdRet==-0]=0
macdWinRate=len(macdRet[macdRet>0])/len(macdRet[macdRet!=0])
macdWinRate


AllSignal=SmaSignal+SLSignal+macdSignal
for i in AllSignal.index:
    if AllSignal[i]>1:
        AllSignal[i]=1
    elif AllSignal[i]<-1:
        AllSignal[i]=-1
    else:
        AllSignal[i]=0

AllSignal[AllSignal==1]
AllSignal[AllSignal==-1]

tradSig=AllSignal.shift(1).dropna()

CBClose=CBClose[-len(tradSig):]
asset=pd.Series(0.0,index=Close.index)
cash=pd.Series(0.0,index=CBClose.index)
share=pd.Series(0,index=CBClose.index)

#当价格连续两天上升且交易信号没有显示卖出时，
#第一次开账户持有股票
entry=3
cash[:entry]=20000
while entry<len(CBClose):
    cash[entry]=cash[entry-1]
    if all([CBClose[entry-1]>=CBClose[entry-2],\
            CBClose[entry-2]>=CBClose[entry-3],\
            AllSignal[entry-1]!=-1]):
        share[entry]=1000
        cash[entry]= cash[entry]-1000*CBClose[entry]
        break
    entry+=1

#根据sigal买卖股票
i=entry+1
while i<len(tradSig):
    cash[i]=cash[i-1]
    share[i]=share[i-1]
    flag=1
    if tradSig[i]==1:
        share[i]= share[i]+3000
        cash[i]=cash[i]-3000*CBClose[i]

    if all([tradSig[i]==-1,share[i]>0]):
        share[i]= share[i]-1000
        cash[i]=cash[i]+1000*CBClose[i]
    i+=1

asset=cash+share*CBClose

plt.subplot(411)
plt.title("2014-2015年上:中国银行均线交易账户")
plt.plot(CBClose, color='b')
plt.ylabel("Pricce")
plt.subplot(412)
plt.plot(share, color='b')
plt.ylabel("Share")
plt.ylim(0,max(share)+1000)

plt.subplot(413)
plt.plot(asset,label="asset",color='r')
plt.ylabel("Asset")
plt.ylim(min(asset)-5000,max(asset)+5000)

plt.subplot(414)
plt.plot(cash, label="cash",color='g')
plt.ylabel("Cash")
plt.ylim(0,max(cash)+5000)

TradeReturn=(asset[-1]-20000)/20000
TradeReturn
