import statsmodels.tsa.arima_process as sm
from statsmodels.graphics.tsaplots import *

#4.
arma=sm.ArmaProcess([-1,-0.6],[1])
sample=arma.generate_sample(200)

plot_acf(sample,lags=20)
plot_pacf(sample,lags=20)

#5.
arma=sm.ArmaProcess([-1],[1,0.4])
sample=arma.generate_sample(200)
plot_acf(sample,lags=20)
plot_pacf(sample,lags=20)

#6.
import statsmodels.tsa.arima_process as sm
from statsmodels.graphics.tsaplots import *
import numpy as np
import pandas as pd
numbers=np.random.normal(size=100)
numbers=pd.Series(numbers)

numbers.plot()
plot_acf(numbers,lags=20)

from statsmodels.tsa import stattools
stattools.arma_order_select_ic(numbers.values,max_ma=4)

#7.
zgsy=pd.read_csv('Data/Part4/003/zgsy.csv')
clprice=zgsy.iloc[:,4]
clprice.plot() 
plot_acf(clprice,lags=20)
from arch.unitroot import ADF
adf=ADF(clprice,lags=6)
print(adf.summary().as_text())

logReturn=pd.Series((np.log(clprice))).diff().dropna()
logReturn.plot() 

adf=ADF(logReturn,lags=6)
print(adf.summary().as_text())

plot_acf(logReturn,lags=20)
plot_pacf(logReturn,lags=20)

from statsmodels.tsa import arima_model
model1=arima_model.ARIMA(logReturn.values,order=(0,0,1)).fit()
model1.summary()

model2=arima_model.ARIMA(logReturn.values,order=(1,0,0)).fit()
model2.summary()

#8.
baiyun=zgsy=pd.read_csv('Data/Part4/003/baiyun.csv',index_col='Date')
baiyun.index=pd.to_datetime(baiyun.index)
clprice=baiyun.Close

logReturn=pd.Series((np.log(clprice))).diff().dropna()
logReturn.plot() 

adf=ADF(logReturn,lags=6)
print(adf.summary().as_text())

plot_acf(logReturn,lags=20)
plot_pacf(logReturn,lags=20)
model1=arima_model.ARIMA(logReturn.values,order=(0,0,2)).fit()
model2=arima_model.ARIMA(logReturn.values,order=(2,0,0)).fit()
model1.aic 
model2.aic

import math
stdresid=model2.resid/math.sqrt(model2.sigma2)
stdresid.plot() 
plot_acf(stdresid,lags=20)
LjungBox=stattools.q_stat(stattools.acf(stdresid)[1:13],len(stdresid))
LjungBox[1][-1] 

pd.Series(model2.forecast(10)[0]).plot() 