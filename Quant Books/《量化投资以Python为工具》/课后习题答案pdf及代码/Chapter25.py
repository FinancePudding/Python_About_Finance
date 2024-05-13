import pandas as pd

#3.
CRSPday=pd.read_csv('Data/Part4/004/CRSPday.csv')
ibm=CRSPday.ibm
ibm.plot() 

from statsmodels.graphics.tsaplots import *
plot_acf(ibm**2,lags=20)

from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(ibm**2)[1:13],len(ibm))
LjungBox[1][-1] 

#4.
import pandas_datareader.data as web
import datetime as dt
google = web.DataReader('GOOGL','yahoo',
   dt.datetime(2004,1,1),dt.datetime(2015,12,31))
google = google.asfreq('M','ffill','end')
googleRet = (google.Close-google.Close.shift(1))/google.Close.shift(1)
googleRet = googleRet.dropna()

googleRet.plot() 
plot_acf(googleRet,lags=20)
plot_pacf(googleRet,lags=20)

LjungBox=stattools.q_stat(stattools.acf(googleRet)[1:13],len(googleRet))
LjungBox[1][-1] 

(googleRet**2).plot() 
plot_acf(googleRet**2,lags=20)
plot_pacf(googleRet**2,lags=20)

LjungBox=stattools.q_stat(stattools.acf(googleRet**2)[1:13],len(googleRet))
LjungBox[1][-1] 

from arch import arch_model
am = arch_model(googleRet)
model = am.fit(update_freq=0) 
print(model.summary())

#5.
cny = web.DataReader('CNY=X','yahoo',
            dt.datetime(2015,1,1),dt.datetime(2015,12,31))
            
ret = (cny.Close-cny.Close.shift(1))/cny.Close.shift(1)
ret = ret.dropna()

cny.Close.plot() 

ret.plot() 
plot_acf(ret,lags=20)
plot_pacf(ret,lags=20)

LjungBox=stattools.q_stat(stattools.acf(ret)[1:13],len(ret))
LjungBox[1][-1] 


(ret**2).plot() 
plot_acf(ret**2,lags=20)
plot_pacf(ret**2,lags=20)

LjungBox=stattools.q_stat(stattools.acf(ret**2)[1:13],len(ret))
LjungBox[1][-1] 

from arch.univariate import ARX,GARCH
model=ARX(ret,lags=1)
model.volatility=GARCH()
res = model.fit() 
print(res.summary())
