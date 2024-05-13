# -*- coding: utf-8 -*-

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import statsmodels.formula.api as smf
import numpy as np
from arch.unitroot import ADF

#1.
zgyh = web.DataReader('601988.SS','yahoo',
                      dt.datetime(2009,1,2),dt.datetime(2012,12,31))

zxyh = web.DataReader('601998.SS','yahoo',
                      dt.datetime(2009,1,2),dt.datetime(2012,12,31))
                      
train_zgyh = zgyh.Close['2009':'2011']
train_zxyh = zxyh.Close['2009':'2011']
train_zxyh.corr(train_zgyh)

trainset=pd.concat([train_zxyh,train_zgyh],1)
trainset.columns=['zxyh','zgyh']

trainset=np.log(trainset)

model = smf.ols('zgyh~zxyh',data=trainset).fit()
resid = model.resid
adf=ADF(resid,trend='nc')
print(adf.summary().as_text())

spread = trainset.zgyh - trainset.zxyh
resid.describe()

#3.
sh50 = pd.read_csv('Data/Part5/001/sh50.csv')
code = sh50.Code[:20]

#定义计算SSD函数
def pair(a):
    if len(a) == 2:
        stock_a = web.DataReader('%d.SS' % a[0],'yahoo',
                      dt.datetime(2015,1,1),dt.datetime(2015,6,30))
        stock_b = web.DataReader('%d.SS' % a[1],'yahoo',
                      dt.datetime(2015,1,1),dt.datetime(2015,6,30))
        x = np.log(stock_a.Close)
        y = np.log(stock_b.Close)
        ret_x = x.diff()[1:]
        ret_y = y.diff()[1:]
        standard_x = (1+ret_x).cumprod()
        standard_y = (1+ret_y).cumprod()
        SSD = ((standard_x-standard_y)**2).sum()
        return(pd.DataFrame({'SSD':[SSD],'stock1':[a[0]],'stock2':[a[1]]}))
    else:
        dat = pd.DataFrame({'SSD':[0],'stock1':[0],'stock2':[0]})
        for i in range(1,len(a)):
            dat = dat.append(pair([a[0],a[i]]))
        return(dat.append(pair(a[1:])))

pair_SSD = pair(code.values)
pair_SSD = pair_SSD[pair_SSD.SSD!=0]
pair_SSD[pair_SSD.SSD<=1]