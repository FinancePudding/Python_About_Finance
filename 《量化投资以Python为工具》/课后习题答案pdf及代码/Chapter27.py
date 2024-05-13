# -*- coding: utf-8 -*-
#1.
import pandas as pd
import numpy as np
import candle as cd
import matplotlib.pyplot as plt

shzheng = pd.read_csv('Data/Part5/001/problem27-1.csv',
                index_col='date')              
shzheng.index.name='Date'
shzheng.index = pd.to_datetime(shzheng.index,format='%Y-%m-%d')
shzheng13=shzheng['2013-03-01':'2013-05-31']
cd.candleVolume(shzheng13,
		candletitle='Candle Plot of Shanghai Composite Index',
		bartitle='volume')


#2.
shzheng = pd.read_csv('Data/Part5/001/problem27-2.csv',
                index_col='date')               
shzheng.index.name='Date'
shzheng.index = pd.to_datetime(shzheng.index,format='%Y-%m-%d')
shzheng131=shzheng['2013-01-01':'2013-06-30']

CL_OP = shzheng131.Close - shzheng131.Open
CL_OP.describe()
Doji = pd.Series(np.where(np.abs(CL_OP.values)<8,1,0),
	index=CL_OP.index)
Doji[Doji==1].index 

cd.candlePlot(shzheng131,
	title='Candle Plot of Shanghai Composite Index')
 
 
#3.
shzheng = pd.read_csv('Data/Part5/001/problem27-3.csv',
                index_col='date')
                
shzheng.index.name='Date'

shzheng.index = pd.to_datetime(shzheng.index,format='%Y-%m-%d')

CL_OP = shzheng.Close - shzheng.Open

CL_OP.describe()

dat = pd.concat([CL_OP,CL_OP.shift(1),CL_OP.shift(2)],1)

candle = np.all([np.abs(dat.iloc[:,1])<=3,dat.iloc[:,2]>11,
                 dat.iloc[:,0]<-6,
                 np.abs(dat.iloc[:,0])<np.abs(dat.iloc[:,2])/2],
                 0)

dataCOP = pd.concat([shzheng.Close,shzheng.Open.shift(1),
                     shzheng.Close.shift(1),shzheng.Open.shift(2)],1)
                     
Doji = np.all([dataCOP.iloc[:,1]>dataCOP.iloc[:,3],dataCOP.iloc[:,1]>dataCOP.iloc[:,0],
               dataCOP.iloc[:,2]>dataCOP.iloc[:,3],dataCOP.iloc[:,2]>dataCOP.iloc[:,0]],0)              
ret = (shzheng.Close-shzheng.Close.shift(1))/shzheng.Close.shift(1)
trend = np.all([ret.shift(2)>0,ret.shift(1)>0],0)

signal = np.all([candle,Doji,trend],0)
sum(signal)

#4.
shzheng = pd.read_csv('Data/Part5/001/problem27-4.csv',
                index_col='date')
                
shzheng.index.name='Date'
shzheng.index = pd.to_datetime(shzheng.index,format='%Y-%m-%d')
CL_OP = shzheng.Close - shzheng.Open
candle = np.all([CL_OP<0,CL_OP.shift(1)>0],0)
diffPrice = np.all([shzheng.Open>shzheng.Close.shift(1),shzheng.Close<shzheng.Open.shift(1)],0)
ret = (shzheng.Close-shzheng.Close.shift(1))/shzheng.Close.shift(1)
trend = np.all([ret.shift(2)>0,ret.shift(1)>0],0)
signal = np.all([candle,diffPrice,trend],0)
sum(signal)

#5.
CL_OP.describe()
candle = np.all([CL_OP<0,CL_OP.shift(1)>17],0)
diffPrice = np.all([shzheng.Close<shzheng.Open.shift(1)],0)
trend = np.all([ret.shift(1)>0,ret.shift(2)>0],0)
signal = pd.Series(np.all([candle,diffPrice,trend],0),index=CL_OP.index)
signal[signal==True]

cd.candlePlot(shzheng['2011-01-01':'2011-02-15'],'2011-01-20')
cd.candlePlot(shzheng['2011-04-15':'2011-05-15'],'2011-05-04')
cd.candlePlot(shzheng['2011-09-15':'2011-10-15'],'2011-09-22')

