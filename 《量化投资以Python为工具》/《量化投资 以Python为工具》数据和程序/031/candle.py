import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY,date2num
from matplotlib.finance import  candlestick_ohlc
import numpy as np


def candlePlot(seriesData,title="a"):
	#设定日期格式
    Date=[date2num(date) for date in seriesData.index]
    seriesData.loc[:,'Date']=Date
    listData=[]
    for i in range(len(seriesData)):
        a=[seriesData.Date[i],\
        seriesData.Open[i],seriesData.High[i],\
        seriesData.Low[i],seriesData.Close[i]]
        listData.append(a)

	#设定绘图相关参数
    ax = plt.subplot()
    mondays = WeekdayLocator(MONDAY)
    #日期格式为‘15-Mar-09’形式
    weekFormatter = DateFormatter('%y %b %d')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(weekFormatter)

	#调用candlestick_ohlc函数
    candlestick_ohlc(ax,listData, width=0.7,\
                     colorup='r',colordown='g')
    ax.set_title(title) #设定标题
    #设定x轴日期显示角度
    plt.setp(plt.gca().get_xticklabels(), \
    rotation=50,horizontalalignment='center')
    return(plt.show())

#蜡烛图与线图
def candleLinePlots(candleData,candleTitle='a',**kwargs):
    Date=[date2num(date) for date in candleData.index]
    candleData.loc[:,'Date']=Date
    listData=[]
    for i in range(len(candleData)):
        a=[candleData.Date[i],\
        candleData.Open[i],candleData.High[i],\
        candleData.Low[i],candleData.Close[i]]
        listData.append(a)
    
    #如果不定长参数无取值，只画蜡烛图
    ax = plt.subplot()

	#如果不定长参数有值，则分成两个子图
    flag=0

    if kwargs:
        for key in kwargs:
    #如果无参数splitFigures，则只画一个图形框
    #如果有参数splitFigures，则画出两个图形框
            if key =='splitFigures':
                ax = plt.subplot(211)
                ax2= plt.subplot(212)
                flag=1
            
            if key=='title':
                ax2.set_title(kwargs[key])
            if key=='ylabel':
                ax2.set_ylabel(kwargs[key])
            if key=='grid':
                ax2.grid(kwargs[key])
            if key =='Data':
                plt.sca(ax)
                if flag:
                    plt.sca(ax2)
                    #一维数据
                if kwargs[key].ndim==1:
                    plt.plot(kwargs[key],\
                       color='k',\
                       label=kwargs[key].name)
                    plt.legend(loc='best')
                    #二维数据有2个columns
                elif all([kwargs[key].ndim==2,\
                         len(kwargs[key].columns)==2]):
                    plt.plot(kwargs[key].iloc[:,0],\
                        linestyle='dashed',\
                        label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],\
                        linestyle='dashed',\
                        label=kwargs[key].iloc[:,1].name)
                    plt.legend(loc='best')
                    #二维数据有3个columns
                elif all([kwargs[key].ndim==2,\
                         len(kwargs[key].columns)==3]):
                    plt.plot(kwargs[key].iloc[:,0],\
                        linestyle='dashed',\
                        label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],\
                        linestyle='dashed',\
                        label=kwargs[key].iloc[:,1].name)
                    plt.bar(left=kwargs[key].iloc[:,2].index,\
                        height=kwargs[key].iloc[:,2],\
                        color='r',\
                        label=kwargs[key].iloc[:,2].name)
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
             rotation=45,\
             horizontalalignment='center')
    #ax.autoscale_view()
    plt.show()
    return(1)

#蜡烛图与成交量柱状图
def candleVolume(seriesData,candletitle='a',bartitle='b'):
    Date=[date2num(date) for date in seriesData.index]
    seriesData.index=list(range(len(Date)))
    seriesData['Date']=Date
    listData=zip(seriesData.Date,seriesData.Open,seriesData.High,seriesData.Low,
                 seriesData.Close)
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    for ax in ax1,ax2:
        mondays = WeekdayLocator(MONDAY)
        weekFormatter = DateFormatter('%m/%d/%Y')
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(DayLocator())
        ax.xaxis.set_major_formatter(weekFormatter)
        ax.grid(True)

    ax1.set_ylim(seriesData.Low.min()-2,seriesData.High.max()+2)
    ax1.set_ylabel('蜡烛图及收盘价线')
    candlestick_ohlc(ax1,listData, width=0.7,colorup='r',colordown='g')
    plt.setp(plt.gca().get_xticklabels(),\
            rotation=45,horizontalalignment='center')
    ax1.autoscale_view()
    ax1.set_title(candletitle)
    ax1.plot(seriesData.Date,seriesData.Close,\
               color='black',label='收盘价')
    ax1.legend(loc='best')

    ax2.set_ylabel('成交量')
    ax2.set_ylim(0,seriesData.Volume.max()*3)
    ax2.bar(np.array(Date)[np.array(seriesData.Close>=seriesData.Open)]
    ,height=seriesData.iloc[:,4][np.array(seriesData.Close>=seriesData.Open)]
    ,color='r',align='center')
    ax2.bar(np.array(Date)[np.array(seriesData.Close<seriesData.Open)]
    ,height=seriesData.iloc[:,4][np.array(seriesData.Close<seriesData.Open)]
    ,color='g',align='center')
    ax2.set_title(bartitle)
    return(plt.show())