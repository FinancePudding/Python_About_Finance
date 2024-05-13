'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 5\\027')
'''

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY,date2num
from datetime import datetime
from matplotlib.finance import  candlestick_ohlc

ssec2015=pd.read_csv(r'E:\Python Quant Book\part 5\027\ssec2015.csv')
ssec2015=ssec2015.iloc[:,1:]
ssec2015.head(n=3)
ssec2015.iloc[-3:,:]
ssec2015.Date=[date2num(datetime.strptime(date,"%Y-%m-%d"))\
               for date in ssec2015.Date]
                  
type(ssec2015)                  
ssec15list=list()
for i in range(len(ssec2015)):
    ssec15list.append(ssec2015.iloc[i,:])

ax= plt.subplot()
mondays = WeekdayLocator(MONDAY)
weekFormatter = DateFormatter('%y %b %d')
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(DayLocator() )
ax.xaxis.set_major_formatter(weekFormatter)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
ax.set_title("上证综指2015年3月份K线图")
candlestick_ohlc(ax, ssec15list, width=0.7,colorup='r', colordown='g')
plt.setp(plt.gca().get_xticklabels(),rotation=50, horizontalalignment='center')
plt.show()



#morning star
ssec2012=pd.read_csv('ssec2012.csv')
ssec2012.index=ssec2012.iloc[:,1]
ssec2012.index=pd.to_datetime(ssec2012.index, format='%Y-%m-%d')
ssec2012=ssec2012.iloc[:,2:]
ssec2012.head(2)
ssec2012.iloc[-2:,:]
Close=ssec2012.Close
Open=ssec2012.Open
ClOp=Close-Open
ClOp.head()
ClOp.describe()
Shape = [0,0,0]
lag1ClOp=ClOp.shift(1)
lag2ClOp=ClOp.shift(2)

for i in range(3,len(ClOp),1):
    if all([lag2ClOp[i]<-11,abs(lag1ClOp[i])<2,\
    ClOp[i]>6,abs(ClOp[i])>abs(lag2ClOp[i]*0.5)]):
        Shape.append(1)
    else:
        Shape.append(0)

Shape.index(1)


lagOpen=Open.shift(1)
lagClose=Close.shift(1)
lag2Close=Close.shift(2)

Doji=[0,0,0]
for i in range(3,len(Open),1):
    if all([lagOpen[i]<Open[i],lagOpen[i]<lag2Close[i],\
    lagClose[i]<Open[i],(lagClose[i]<lag2Close[i])]):
        Doji.append(1)
    else:
        Doji.append(0)
Doji.count(1)

ret=Close/Close.shift(1)-1
lag1ret=ret.shift(1)
lag2ret=ret.shift(2)
Trend=[0,0,0]
for i in range(3,len(ret)):
    if all([lag1ret[i]<0,lag2ret[i]<0]):
        Trend.append(1)
    else:
        Trend.append(0)

StarSig=[]
for i in range(len(Trend)):
    if all([Shape[i]==1,Doji[i]==1,Trend[i]==1]):
        StarSig.append(1)
    else:
        StarSig.append(0)

for i in range(len(StarSig)):
    if StarSig[i]==1:
        print(ssec2012.index[i])


ssec201209=ssec2012['2012-08-21':'2012-09-30']

# Need to specify path before import
import candle
candle.candlePlot(ssec201209 ,title=' 上 证 综 指 2012 年9 月 份 的 日 K 线图 ')

# Dark Cloud Cover
# 提 取 读 入 上 证 综 指 年 的 日 交 易 数 据
import pandas as pd
ssec2011=pd.read_csv('ssec2011.csv')
ssec2011.index=ssec2011.iloc[:,1]
ssec2011.index=pd.to_datetime(ssec2011.index, format='%Y-%m-%d')
ssec2011=ssec2011.iloc[:,2:]

# 提 取 价 格 数 据
Close11=ssec2011.Close
Open11=ssec2011.Open

# 刻 画 捕 捉 符 合 “ 乌 云 盖 顶 ” 形 态 的 连 续 两 个 蜡 烛 实 体
lagClose11=Close11.shift(1)
lagOpen11=Open11.shift(1)
Cloud=pd.Series(0,index=Close11.index)
for i in range(1,len(Close11)):
    if all([Close11[i]<Open11[i],\
            lagClose11[i]>lagOpen11[i],\
            Open11[i]>lagClose11[i],\
            Close11[i]<0.5*(lagClose11[i]+lagOpen11[i]),\
            Close11[i]>lagOpen11[i]]):
        Cloud[i]=1

# 定 义 前 期 上 升 趋 势
Trend=pd.Series(0,index=Close11.index)
for i in range(2,len(Close11)):
    if Close11[i-1]>Close11[i-2]>Close11[i-3]:
        Trend[i]=1

darkCloud=Cloud+Trend
darkCloud[darkCloud==2]

# 绘 制 上 证 综 指 2011 年5月 19 日 附 近 的 K 线图
ssec201105=ssec2011['2011-05-01':'2011-05-30']           
candle.candlePlot(ssec201105 ,\
                  title=' 上 证 综 指 2011 年5 月 份 的 日 K 线图 ')

# 绘 制 上 证 综 指 2011 年8月 16 日 附 近 的 K 线图
ssec201108=ssec2011['2011-08-01':'2011-08-30']
candle.candlePlot(ssec201108 ,\
                  title=' 上 证 综 指 2011 年8 月 份 的 日 K 线图 ')


