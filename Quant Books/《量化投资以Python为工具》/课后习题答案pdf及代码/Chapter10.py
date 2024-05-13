# -*- coding: utf-8 -*-
#1.
import numpy as np
hilbert = 1/(np.arange(4)+np.arange(1,5)[:,np.newaxis])

#2.
import datetime as dt
import numpy as np
import datetime as dt
import math
dates = [dt.datetime(2015,1,13)+dt.timedelta(i) for i in range(5)]
closes = [7.31,7.28,7.40,7.43,7.41]
prices = {dates[i]:closes[i] for i in range(5)}
prices[dt.datetime(2015,1,20)] = 7.44
dates.append(dt.datetime(2015,1,20))
cash = 10000
share = {dates[0]:0}
for i in range(1,6):
    if prices[dates[i]]>prices[dates[i-1]]:
        buyshare = math.floor(0.5*cash/prices[dates[i]])
        share[dates[i]]= buyshare
        cash=cash-buyshare*prices[dates[i]]+share[dates[i-1]]*prices[dates[i]]
    else:
         share[dates[i]]= 0
buyDates=[np.datetime64(date) for date in share.keys() if share[date]>0]
buyDates
[prices[dt.datetime.
         strptime(np.datetime_as_string(date)[:10],
         	"%Y-%m-%d")] for date in buyDates]

#3.
cosin = np.cos(np.linspace(0,2*np.pi,1001))

#4.
sample = np.array([0.5,1.43,-1.36,-0.16,0.29,-0.59,
	              1.16,-0.33,0.07,-1.36])

np.mean(sample)
np.var(sample)
np.std(sample)
np.median(sample)