# -*- coding: utf-8 -*-

#9.
import pandas_datareader.data as web

import datetime as dt

import numpy as np

start = dt.datetime(2014,1,1)

end = dt.datetime(2014,12,31)

baidu = web.DataReader('BIDU','yahoo',start,end)

returns = (baidu.Close - baidu.Close.shift(1))/baidu.Close.shift(1)

comp_returns = np.log(baidu.Close/baidu.Close.shift(1))

comp_returns.sum()

returns.plot()

comp_returns.plot()