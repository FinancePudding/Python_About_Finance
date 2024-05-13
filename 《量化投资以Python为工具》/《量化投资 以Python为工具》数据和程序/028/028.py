'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\028')
'''

import pandas as pd
import matplotlib.pyplot as plt


Vanke=pd.read_csv('Vanke.csv')
Vanke.index=Vanke.iloc[:,1]
Vanke.index=pd.to_datetime(Vanke.index, format='%Y-%m-%d')
Vanke=Vanke.iloc[:,2:]
Vanke.head(2)

Close=Vanke.Close
Close.describe()
lag5Close=Close.shift(5)

momentum5=Close-lag5Close
momentum5.tail()


#plot
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.subplot(211)
plt.plot(Close,'b*')
plt.xlabel('date')
plt.ylabel('Close')
plt.title('万科股价5日动量图')

plt.subplot(212)
plt.plot(Close,'r-*')
plt.xlabel('date')
plt.ylabel('Momentum5')


#divide
Momen5=Close/lag5Close-1
Momen5=Momen5.dropna();
Momen5[0:5]


#momentum function
def momentum(price,periond):
    lagPrice=price.shift(periond)
    momen=price-lagPrice
    momen= momen.dropna()
    return(momen)

momentum(Close,5).tail(n=5)

momen35=momentum(Close,35)


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, \
                                DayLocator, MONDAY, date2num
from matplotlib.finance import candlestick_ohlc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义 candleLinePlots 函数
def candleLinePlots(candleData, candleTitle='a', **kwargs):
    Date = [date2num(date) for date in candleData.index]
    candleData.loc[:,'Date'] = Date
    listData = []
    
    for i in range(len(candleData)):
        a = [candleData.Date[i]],\
            candleData.Open[i],candleData.High[i],\
            candleData.Low[i],candleData.Close[i]]
            listData.append(a)
    # 如 果 不 定 长 参 数 无 取 值 ， 只 画 蜡 烛 图
    ax = plt.subplot()
    
    # 如 果 不 定 长 参 数 有 值 ， 则 分 成 两 个 子 图
    flag=0
    if kwargs:
        if kwargs['splitFigures']:
            ax = plt.subplot(211)
            ax2= plt.subplot(212)
            flag=1;
        # 如 果 无 参 数 splitFigures ， 则 只 画 一 个 图 形 框
        # 如 果 有 参 数 splitFigures ， 则 画 出 两 个 图 形 框
        
        for key in kwargs:
            if key=='title':
                ax2.set_title(kwargs[key])
            if key=='ylabel':
                ax2.set_ylabel(kwargs[key])
            if key=='grid':
                ax2.grid(kwargs[key])
            if key=='Data':
                plt.sca(ax)
                if flag:
                    plt.sca(ax2)
                    
                #一维数据
                if kwargs[key].ndim==1:
                    plt.plot(kwargs[key],\
                             color='k',\
                             label=kwargs[key].name)
                    plt.legend(loc='best')
                #二维数据有两个columns
                elif all([kwargs[key].ndim==2,\
                          len(kwargs[key].columns)==2]):
                    plt.plot(kwargs[key].iloc[:,0], color='k', 
                             label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],\
                             linestyle='dashed',\
                             label=kwargs[key].iloc[:,1].name)
                    plt.legend(loc='best')
    
    mondays = WeekdayLocator(MONDAY)
    weekFormatter = DateFormatter('%y %b %d')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(weekFormatter)
    plt.sca(ax)
    
    candlestick_ohlc(ax,listData, width=0.7,\
                     colorup='r',colordown='g')
    ax.set_title(candleTitle)
    plt.setp(ax.get_xticklabels(),\
             rotation=20,\
             horizontalalignment='center')
    ax.autoscale_view()
    
    return(plt.show())
                

#Candle 模组是本书自己编的模组，里面有绘制K线函数Candleplot
import candle
Vanke15=Vanke['2015']
candle.candleLinePlots(Vanke['2015'],\
               candleTitle='万科股票2015年日K线图',\
               splitFigures=True,Data=momen35['2015'],\
               title='35日动量',ylabel='35日动量')


Close=Vanke.Close
momen35=momentum(Close,35)
momen35.head()
signal=[]
for i in momen35:
    if i>0:
        signal.append(1)
    else:
        signal.append(-1)

signal=pd.Series(signal,index=momen35.index)
signal.head()
tradeSig = signal.shift(1)
ret=Close/Close.shift(1)-1
# ret=ret['2014-02-20':]
# ret.head(n=3)
Mom35Ret=ret*(signal.shift(1))
Mom35Ret[0:5]
real_Mom35Ret=Mom35Ret[Mom35Ret!=0]
real_ret=ret[ret!=0]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.subplot(2,1,1)
plt.plot(real_ret,'b')
plt.ylabel('return')
plt.title('万科收益率时序图')

plt.subplot(2,1,2)
plt.plot(Mom35Ret,'r')
plt.ylabel('Mom35Ret')
plt.title('万科动量交易收益率时序图')

win=Mom35Ret[Mom35Ret>0]
winrate=len(win)/len(Mom35Ret)
winrate

loss=-Mom35Ret[Mom35Ret<0]
plt.subplot(2,1,1)
win.hist()
plt.title("盈利直方图")

plt.subplot(2,1,2)
loss.hist()
plt.title("损失直方图")

performance=pd.DataFrame({"win":win.describe(),\
"loss":loss.describe()})
performance