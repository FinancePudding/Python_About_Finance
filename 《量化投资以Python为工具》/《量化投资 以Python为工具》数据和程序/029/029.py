import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


BOCM=pd.read_csv('029/BOCM.csv')
BOCM.index=BOCM.iloc[:,1]
BOCM.index=pd.to_datetime(BOCM.index, format='%Y-%m-%d')
BOCM=BOCM.iloc[:,2:]
BOCM.head()


BOCMclp=BOCM.Close
clprcChange=BOCMclp-BOCMclp.shift(1)
clprcChange=clprcChange.dropna()
clprcChange[0:6]

indexprc=clprcChange.index
upPrc=pd.Series(0,index=indexprc)
upPrc[clprcChange>0]=clprcChange[clprcChange>0]
downPrc=pd.Series(0,index=indexprc)
downPrc[clprcChange<0]=-clprcChange[clprcChange<0]
rsidata=pd.concat([BOCMclp,clprcChange,upPrc,downPrc],axis=1)
rsidata.columns=['Close','PrcChange','upPrc','downPrc']
rsidata=rsidata.dropna();
rsidata.head()

SMUP=[]
SMDOWN=[]
for i in range(6,len(upPrc)+1):
    SMUP.append(np.mean(upPrc.values[(i-6):i],dtype=np.float32))
    SMDOWN.append(np.mean(downPrc.values[(i-6):i],dtype=np.float32))

rsi6=[100*SMUP[i]/(SMUP[i]+SMDOWN[i]) for i in range(0,len(SMUP))]

indexRsi=indexprc[5:]
Rsi6=pd.Series(rsi6,index=indexRsi)
Rsi6.head()
Rsi6.describe()



UP=pd.Series(SMUP,index=indexRsi)
DOWN=pd.Series(SMDOWN,index=indexRsi)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.subplot(411)
plt.plot(BOCMclp,'k')
plt.xlabel('date')
plt.ylabel('Close')
plt.title('RSI相关指标')
plt.subplot(412)
plt.plot(UP,'b')
plt.ylabel('UP')
plt.subplot(413)
plt.plot(DOWN,'y')
plt.ylabel('DOWN')
plt.subplot(414)
plt.plot(DOWN,'g')
plt.ylabel('Rsi6')

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


Rsi12=rsi(BOCMclp,12)
Rsi12.tail()

Rsi24=rsi(BOCMclp,24)
Rsi24.tail()


plt.plot(Rsi6)
plt.title('RSI6指标超买和超卖')
plt.ylim(-10,110)
plt.axhline(y=80,color='red')
plt.axhline(y=20,color='red')
plt.show()

#黄金交叉与死亡交叉
plt.plot(Rsi6['2015-01-03':],label="Rsi6")
plt.plot(Rsi24['2015-01-03':],\
         label="Rsi24",color='red',\
         linestyle='dashed')
plt.title("RSI的黄金交叉与死亡交叉")
plt.ylim(-10,110)
plt.legend()


#strategy
BOCM=pd.read_csv('029/BOCM.csv')
BOCM.index=BOCM.iloc[:,1]
BOCM.index=pd.to_datetime(BOCM.index, format='%Y-%m-%d')
BOCMclp=BOCM.Close
BOCMclp[0:4]

rsi6=rsi(BOCMclp,6)
rsi24=rsi(BOCMclp,24)

#rsi6捕捉买卖点
Sig1=[]
for i in rsi6:
    if i>80:
        Sig1.append(-1)
    elif i<20:
        Sig1.append(1)
    else:
        Sig1.append(0)

date1=rsi6.index
Signal1=pd.Series(Sig1,index=date1)
Signal1[Signal1==1].head(n=3)
Signal1[Signal1==-1].head(n=3)

Signal2=pd.Series(0,index=rsi24.index)
lagrsi6= rsi6.shift(1)
lagrsi24= rsi24.shift(1)
for i in rsi24.index:
    if (rsi6[i]>rsi24[i]) & (lagrsi6[i]<lagrsi24[i]):
        Signal2[i]=1
    elif (rsi6[i]<rsi24[i]) & (lagrsi6[i]>lagrsi24[i]):
        Signal2[i]=-1

signal=Signal1+Signal2
signal[signal>=1]=1
signal[signal<=-1]=-1
signal=signal.dropna()

tradSig=signal.shift(1)

ret=BOCMclp/BOCMclp.shift(1)-1
ret.head()

ret=ret[tradSig.index]
buy=tradSig[tradSig==1]
buyRet=ret[tradSig==1]*buy

sell=tradSig[tradSig==-1]
sellRet=ret[tradSig==-1]*sell

tradeRet=ret*tradSig

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.subplot(211)
plt.plot(buyRet,label="buyRet",color='g')
plt.plot(sellRet,label="sellRet",color='r',linestyle='dashed')
plt.title("RSI指标交易策略")
plt.ylabel('strategy return')
plt.legend()
plt.subplot(212)
plt.plot(ret,'b')
plt.ylabel('stock return')

def strat(tradeSignal,ret):
    indexDate=tradeSignal.index
    ret=ret[indexDate]
    tradeRet=ret*tradeSignal
    tradeRet[tradeRet==(-0)]=0
    winRate=len(tradeRet[tradeRet>0])/len(\
    tradeRet[tradeRet!=0])
    meanWin=sum(tradeRet[tradeRet>0])/len(\
    tradeRet[tradeRet>0])
    meanLoss=sum(tradeRet[tradeRet<0])/len(\
    tradeRet[tradeRet<0])
    perform={'winRate':winRate,\
    'meanWin':meanWin,\
    'meanLoss': meanLoss}
    return(perform)

BuyOnly=strat(buy,ret)
SellOnly=strat(sell,ret)
Trade=strat(tradSig,ret)
Test=pd.DataFrame({"BuyOnly":BuyOnly,\
        "SellOnly":SellOnly,"Trade":Trade})
Test

#累计收益率
cumStock=np.cumprod(1+ret)-1
cumTrade=np.cumprod(1+tradeRet)-1

plt.subplot(211)
plt.plot(cumStock)
plt.ylabel('cumStock')
plt.title('股票本身累计收益率')
plt.subplot(212)
plt.plot(cumTrade)
plt.ylabel('cumTrade')
plt.title('rsi策略累计收益率')


#修正策略
tradSig2=signal.shift(3)
ret2=ret[tradSig2.index]
buy2=tradSig[tradSig2==1]
buyRet2=ret2[tradSig2==1]*buy2
sell2=tradSig2[tradSig2==-1]
sellRet2=ret2[tradSig2==-1]*sell2
tradeRet2=ret2*tradSig2
BuyOnly2=strat(buy2,ret2)
SellOnly2=strat(sell2,ret2)
Trade2=strat(tradSig2,ret2)
Test2=pd.DataFrame({"BuyOnly":BuyOnly2,\
      "SellOnly":SellOnly2,"Trade":Trade2})
Test2

cumStock2=np.cumprod(1+ret2)-1
print(cumStock2[-1])
cumTrade2=np.cumprod(1+tradeRet2)-1
print(cumTrade2[-1])

plt.subplot(211)
plt.plot(cumStock2)
plt.ylabel('cumStock2')
plt.title('股票本身累计收益率')
plt.subplot(212)
plt.plot(cumTrade2)
plt.ylabel('cumTrade2')
plt.title('修改rsi执行策略累计收益率')
