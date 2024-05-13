'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 4\\026')
'''

import pandas as pd

import matplotlib.pyplot as plt
import math
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='C:/Windows/Fonts/msyh.ttf')

#导入ADF函数和numpy包
from arch.unitroot import ADF
import numpy as np

import re
import statsmodels.api as sm

from statsmodels.tsa.stattools import adfuller

sh=pd.read_csv('sh50p.csv',index_col='Trddt')
sh.index=pd.to_datetime(sh.index)

formStart='2014-01-01'
formEnd='2015-01-01'
shform=sh[formStart:formEnd]
shform.head(n=2) 

#中國聯通，中國銀行
PAf=shform['601988']
PBf=shform['600000']
pairf=pd.concat([PAf,PBf],axis = 1)
len(pairf)
pairf.plot()

def SSD(priceX,priceY):
    if priceX is None or priceY is None:
        print('缺少价格序列.')
    returnX=(priceX-priceX.shift(1))/priceX.shift(1)[1:]
    returnY=(priceY-priceY.shift(1))/priceY.shift(1)[1:]
    standardX=(returnX+1).cumprod()
    standardY=(returnY+1).cumprod()
    SSD=np.sum((standardX-standardY)**2)
    return(SSD) 
    
dis=SSD(PAf,PBf)
dis


PAflog=np.log(PAf)
adfA=ADF(PAflog)

print(adfA.summary().as_text())

retA=PAflog.diff()[1:]

adfretA=ADF(retA)
print(adfretA.summary().as_text())

PBflog=np.log(PBf)

adfB=ADF(PBflog)

print(adfB.summary().as_text())

retB=PBflog.diff()[1:]

adfretB=ADF(retB)

print(adfretB.summary().as_text())

PAflog.plot(label='601988',style='--')
PBflog.plot(label='600000',style='-')
plt.legend(loc='upper left')
plt.title('中国银行与浦发银行的对数价格时序图') 

retA.plot(label='601988',style='--')
retB.plot(label='600000',style='-')
plt.legend(loc='lower left')
plt.title('中国银行与浦发银行对数价格差分(收益率)') 

#回归分析 
#因变量是中国联通股票的对数价格 
#自变量是中国银行股票的对数价格

model=sm.OLS(PBflog,sm.add_constant(PAflog))

results=model.fit()

print(results.summary())

alpha=results.params[0]  
beta=results.params[1]
spread=PBflog-beta*PAflog-alpha
spread.head()

spread.plot()
plt.title('价差序列') 

adfSpread=ADF(spread, trend='nc') 
print(adfSpread.summary().as_text())

#最小距离法交易策略
#中国联通标准化价格
standardA=(1+retA).cumprod()

#中国银行标准化价格
standardB=(1+retB).cumprod()

#求中国联通与中国银行标准化价格序列的价差 
SSD_pair=standardB-standardA

SSD_pair.head() 

meanSSD_pair=np.mean(SSD_pair)

sdSSD_pair=np.std(SSD_pair)

thresholdUp=meanSSD_pair+1.2*sdSSD_pair

thresholdDown=meanSSD_pair-1.2*sdSSD_pair


SSD_pair.plot()
plt.title('中国银行与浦发银行标准化价差序列(形成期)') 
plt.axhline(y=meanSSD_pair,color='black')
plt.axhline(y=thresholdUp,color='green')
plt.axhline(y=thresholdDown,color='green') 

tradStart='2015-01-01'
tradEnd='2015-06-30'

PAt=sh.loc[tradStart:tradEnd,'601988']

PBt=sh.loc[tradStart:tradEnd,'600000']

def spreadCal(x,y):
    retx=(x-x.shift(1))/x.shift(1)[1:]
    rety=(y-y.shift(1))/y.shift(1)[1:]
    standardX=(1+retx).cumprod()
    standardY=(1+rety).cumprod()
    spread=standardX-standardY
    return(spread)

TradSpread=spreadCal(PBt,PAt).dropna()

TradSpread.describe() 
 
TradSpread.plot()
plt.title('交易期价差序列')
plt.axhline(y=meanSSD_pair,color='black')
plt.axhline(y=thresholdUp,color='green')
plt.axhline(y=thresholdDown,color='green') 

spreadf=PBflog-beta*PAflog-alpha
mu=np.mean(spreadf)
sd=np.std(spreadf)
mu+1.2*sd
mu-1.2*sd
#形成期
CoSpreadT=np.log(PBt)-beta*np.log(PAt)-alpha
CoSpreadT.describe() 

CoSpreadT.plot()
plt.title('交易期价差序列(协整配对)')
plt.axhline(y=mu,color='black')
plt.axhline(y=mu+1.2*sd,color='green')
plt.axhline(y=mu-1.2*sd,color='green') 

import pandas as pd

import matplotlib.pyplot as plt
import math
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='C:/Windows/Fonts/msyh.ttf')

#导入ADF函数和numpy包
from arch.unitroot import ADF
import numpy as np

import re
import pandas as pd 
import numpy as np 
from arch.unitroot import ADF
import statsmodels.api as sm

from statsmodels.tsa.stattools import adfuller

class PairTrading:
    def SSD(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少价格序列.')
        returnX=(priceX-priceX.shift(1))/priceX.shift(1)[1:]
        returnY=(priceY-priceY.shift(1))/priceY.shift(1)[1:]
        standardX=(returnX+1).cumprod()
        standardY=(returnY+1).cumprod()
        SSD=np.sum((standardY-standardX)**2)
        return(SSD)
    def SSDSpread(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少价格序列.')
        priceX=np.log(priceX)
        priceY=np.log(priceY)
        retx=priceX.diff()[1:]
        rety=priceY.diff()[1:]
        standardX=(1+retx).cumprod()
        standardY=(1+rety).cumprod()
        spread=standardY-standardX
        return(spread)
    def cointegration(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少价格序列.')
        priceX=np.log(priceX)
        priceY=np.log(priceY)
        results=sm.OLS(priceY,sm.add_constant(priceX)).fit()
        resid=results.resid
        adfSpread=ADF(resid)
        if adfSpread.pvalue>=0.05:
            print('''交易价格不具有协整关系.
            P-value of ADF test: %f
            Coefficients of regression:
            Intercept: %f
            Beta: %f
             ''' % (adfSpread.pvalue, results.params[0], results.params[1]))
            return(None)
        else:
            print('''交易价格具有协整关系.
            P-value of ADF test: %f
            Coefficients of regression:
            Intercept: %f
            Beta: %f
             ''' % (adfSpread.pvalue, results.params[0], results.params[1]))
            return(results.params[0], results.params[1])
    def CointegrationSpread(self,priceX,priceY,formPeriod,tradePeriod):
        if priceX is None or priceY is None:
            print('缺少价格序列.')
        if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',formPeriod)
                or re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',tradePeriod)):
            print('形成期或交易期格式错误.')
        formX=priceX[formPeriod.split(':')[0]:formPeriod.split(':')[1]]
        formY=priceY[formPeriod.split(':')[0]:formPeriod.split(':')[1]]
        coefficients=self.cointegration(formX,formY)
        if coefficients is None:
                print('未形成协整关系,无法配对.')
        else:
            spread=(np.log(priceY[tradePeriod.split(':')[0]:tradePeriod.split(':')[1]])
            -coefficients[0]-coefficients[1]*np.log(priceX[tradePeriod.split(':')[0]:tradePeriod.split(':')[1]]))
            return(spread)
    def calBound(self,priceX,priceY,method,formPeriod,width=1.5):
        if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',formPeriod)
                or re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',tradePeriod)):
            print('形成期或交易期格式错误.')
        if method=='SSD':
            spread=self.SSDSpread(priceX[formPeriod.split(':')[0]:formPeriod.split(':')[1]],
                                  priceY[formPeriod.split(':')[0]:formPeriod.split(':')[1]])            
            mu=np.mean(spread)
            sd=np.std(spread)
            UpperBound=mu+width*sd
            LowerBound=mu-width*sd
            return(UpperBound,LowerBound)
        elif method=='Cointegration':
            spread=self.CointegrationSpread(priceX,priceY,formPeriod,formPeriod)
            mu=np.mean(spread)
            sd=np.std(spread)
            UpperBound=mu+width*sd
            LowerBound=mu-width*sd
            return(UpperBound,LowerBound)
        else:
            print('不存在该方法. 请选择"SSD"或是"Cointegration".')


sh=pd.read_csv('sh50p.csv',index_col='Trddt')
sh.index=pd.to_datetime(sh.index)

formPeriod='2014-01-01:2015-01-01'
tradePeriod='2015-01-01:2015-06-30'

priceA=sh['601988']
priceB=sh['600000']
priceAf=priceA[formPeriod.split(':')[0]:formPeriod.split(':')[1]]
priceBf=priceB[formPeriod.split(':')[0]:formPeriod.split(':')[1]]
priceAt=priceA[tradePeriod.split(':')[0]:tradePeriod.split(':')[1]]
priceBt=priceB[tradePeriod.split(':')[0]:tradePeriod.split(':')[1]]

pt=PairTrading()
SSD=pt.SSD(priceAf,priceBf)
SSD

SSDspread=pt.SSDSpread(priceAf,priceBf)
SSDspread.describe()
SSDspread.head()

coefficients=pt.cointegration(priceAf,priceBf)
coefficients
alpha
beta

CoSpreadF=pt.CointegrationSpread(priceA,priceB,formPeriod,formPeriod)
CoSpreadF.head()


CoSpreadTr=pt.CointegrationSpread(priceA,priceB,formPeriod,tradePeriod)
CoSpreadTr.describe()

bound=pt.calBound(priceA,priceB,'Cointegration',formPeriod,width=1.2)
bound

#配对交易实测
#提取形成期数据
formStart='2014-01-01'
formEnd='2015-01-01'
PA=sh['601988']
PB=sh['600000']

PAf=PA[formStart:formEnd]
PBf=PB[formStart:formEnd]

#形成期协整关系检验
#一阶单整检验
log_PAf=np.log(PAf)
adfA=ADF(log_PAf)
print(adfA.summary().as_text())
adfAd=ADF(log_PAf.diff()[1:])
print(adfAd.summary().as_text())
log_PAf.plot()
log_PAf.diff()[1:].plot()

log_PBf=np.log(PBf)
adfB=ADF(log_PBf)
print(adfB.summary().as_text())
adfBd=ADF(log_PBf.diff()[1:])
print(adfBd.summary().as_text())

#协整关系检验
model=sm.OLS(log_PBf,sm.add_constant(log_PAf)).fit()
model.summary() 

alpha=model.params[0]
alpha 
beta=model.params[1]
beta 

spreadf=log_PBf-beta*log_PAf-alpha



#残差单位根检验
adfSpread=ADF(spreadf)

print(adfSpread.summary().as_text())
  
mu=np.mean(spreadf)
sd=np.std(spreadf)

spreadf.plot()
plt.title('中国石油与工商银行标准化价差序列(形成期)') 
plt.axhline(y=mu,color='black')
plt.axhline(y=mu+1.5*sd,color='green')
plt.axhline(y=mu-1.5*sd,color='green') 

#设定交易期

tradeStart='2015-01-01'
tradeEnd='2015-06-30'

PAt=PA[tradeStart:tradeEnd]
PBt=PB[tradeStart:tradeEnd]

CoSpreadT=np.log(PBt)-beta*np.log(PAt)-alpha

CoSpreadT.describe()


CoSpreadT.plot()
plt.title('交易期价差序列(协整配对)')
plt.axhline(y=mu,color='black')
plt.axhline(y=mu+0.2*sd,color='blue',ls='-',lw=2)
plt.axhline(y=mu-0.2*sd,color='blue',ls='-',lw=2)
plt.axhline(y=mu+1.5*sd,color='green',ls='--',lw=2.5)
plt.axhline(y=mu-1.5*sd,color='green',ls='--',lw=2.5)
plt.axhline(y=mu+2.5*sd,color='red',ls='-.',lw=3) 
plt.axhline(y=mu-2.5*sd,color='red',ls='-.',lw=3) 


level=(float('-inf'),mu-2.5*sd,mu-1.5*sd,mu-0.2*sd,mu+0.2*sd,mu+1.5*sd,mu+2.5*sd,float('inf'))

prcLevel=pd.cut(CoSpreadT,level,labels=False)-3

prcLevel.head() 

def TradeSig(prcLevel):
    n=len(prcLevel)
    signal=np.zeros(n)
    for i in range(1,n):
        if prcLevel[i-1]==1 and prcLevel[i]==2:
            signal[i]=-2
        elif prcLevel[i-1]==1 and prcLevel[i]==0:
            signal[i]=2
        elif prcLevel[i-1]==2 and prcLevel[i]==3:
            signal[i]=3
        elif prcLevel[i-1]==-1 and prcLevel[i]==-2:
            signal[i]=1
        elif prcLevel[i-1]==-1 and prcLevel[i]==0:
            signal[i]=-1
        elif prcLevel[i-1]==-2 and prcLevel[i]==-3:
            signal[i]=-3
    return(signal)

signal=TradeSig(prcLevel)

position=[signal[0]]
ns=len(signal)

for i in range(1,ns):
    position.append(position[-1])
    if signal[i]==1:
        position[i]=1
    elif signal[i]==-2:
        position[i]=-1
    elif signal[i]==-1 and position[i-1]==1:
        position[i]=0
    elif signal[i]==2 and position[i-1]==-1:
        position[i]=0
    elif signal[i]==3:
        position[i]=0
    elif signal[i]==-3:
        position[i]=0

position=pd.Series(position,index=CoSpreadT.index)

position.tail() 

def TradeSim(priceX,priceY,position):
    n=len(position)
    size=1000
    shareY=size*position
    shareX=[(-beta)*shareY[0]*priceY[0]/priceX[0]]
    cash=[2000]
    for i in range(1,n):
        shareX.append(shareX[i-1])
        cash.append(cash[i-1])
        if position[i-1]==0 and position[i]==1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==0 and position[i]==-1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
        elif position[i-1]==-1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
    cash = pd.Series(cash,index=position.index)
    shareY=pd.Series(shareY,index=position.index)
    shareX=pd.Series(shareX,index=position.index)
    asset=cash+shareY*priceY+shareX*priceX
    account=pd.DataFrame({'Position':position,'ShareY':shareY,'ShareX':shareX,'Cash':cash,'Asset':asset})
    return(account)


account1=TradeSim(PAt,PBt,position)
account1.tail() 
account1.ix[-1,'Asset']
account1.iloc[:,(0,1,4)].plot(style=['--','-',':'])
plt.title('配对交易账户') 
account1.iloc[:,(0,3,4)]