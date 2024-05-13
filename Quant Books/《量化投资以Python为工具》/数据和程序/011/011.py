import pandas as pd
import numpy as np

pd.__version__

S1=pd.Series()
S1

S2=pd.Series([1,3,5,7,9], \
    index=['a','b','c','d','e'])
S2
S2.values
S2.index
S2['f']=11
S2

pd.Series({'a': 1,'b': 3,'c': 5,'d': 7})

S3=pd.Series([1, 3, -5, 7])
S3

np.random.seed(54321)
pd.Series(np.random.randn(5))

pd.Series(np.arange(2, 6))

S4=pd.Series([0,np.NaN,2,4,6,8,\
              True, 10, 12])
S4.head()
S4.head(3)
S4.tail()
S4.tail(6)
S4.take([2,4,0])

S5= pd.Series([1,3,5,7,9],\
     index=['a','b','c','d','e'])
S5[2],S5['d']

S5[[1,3,4]]
S5[['b','e','d']]
S5[0:4]
S5['a':'d']

from datetime import datetime
import pandas as pd

date = datetime(2016,1,1)
date = pd.Timestamp(date)
date
type(date)
ts=pd.Series(1,index=[date])
ts
ts.index
ts.index[0]

dates = ['2016-01-01','2016-01-02','2016-01-03']
ts=pd.Series([1,2,3],index=pd.to_datetime(dates))
ts 
ts.index 
ts.index[0] 

dates = [datetime(2016,1,1),datetime(2016,1,2),datetime(2016,1,3)]
ts=pd.Series([1,2,3],index=dates)
ts.index[0] 
ts['20160101']
ts['2016-01-01']
ts['01/01/2016']

ts
ts['2016']
ts['2016-01':'2016-02']
ts.truncate(after='2016-01-02') 
ts.shift(1) #正数为滞后
ts.shift(-1) #负数为超前

price=pd.Series([20.34,20.56,21.01,20.65,21.34],\
                index=pd.to_datetime(['2016-01-01','2016-01-02',\
                '2016-01-03','2016-01-04','2016-01-05']))
(price-price.shift(1))/price.shift(1) 


ts.index.freq is None 
rts=ts.resample('M',how='first') #'M'指的是每月最后一天
rts 
rts=ts.resample('MS',how='first') #'MS'指的是每月的第一天
rts 

import pandas as pd
import numpy as np

dates = ['2016-01-01','2016-01-02','2016-01-03',
         '2016-01-04','2016-01-05','2016-01-06']
dates=pd.to_datetime(dates)
dates

#由于随机的关系，接下来跑出的结果会和书上内容不同
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
df

df.head(3)
df.tail(4)
df.columns
df.index
df.values
df.describe()

df[1:3]
df['A']
df[['A','C']]
df[df['A']>0]
df.loc[:,'A']
df.loc[:,'A':'C']
df.loc[dates[0:2],'A':'C']
df.loc[dates[0],'A']
df.at[dates[0],'A']
df.loc[df.loc[:,'A']>0]

df.iloc[2]
df.iloc[:,2]
df.iloc[[1,4],[2,3]]
df.iloc[1:4,2:4]
df.iloc[3,3]
df.iat[3,3]
df.loc[:,df.iloc[3]>0]

df.ix[2:5]
df.ix[[1,3],2]
df.ix[[1,3],'C']
df.ix[1:3,'A':'C']
df.ix[1:3,df.iloc[3]>0]

df.T
df.sort(axis=0, ascending=False)
df.sort(axis=1, ascending=False)
df.sort(columns='C')
df
df.rank(axis=0)
df.rank(axis=1,ascending=False)

s1=pd.Series([1,2,3,4,5,6],index=pd.date_range('20160102',periods=6))
s1
df['E'] = s1
df
df=df[list('ABCD')]
pd.concat([df, s1], axis=1)

df1=pd.DataFrame({'A':[1,2,3],'B':[4,5,6],'C':[7,8,9]},\
                index=pd.date_range('20160110',periods=3))
df1 
df.append(df1)
pd.concat([df,df1],join='inner')
df.drop(dates[1:3]) 
df.drop('A',axis=1) 
del df['A']
df

df.loc[dates[2],'C'] = 0
df.iloc[0,2] = 0
df.loc[:,'B'] = np.arange(0,len(df))
df

new_index=pd.date_range('20160102',periods=7)
df.reindex(new_index,columns=list('ABCD'))

import pandas as pd 
import numpy as np
s1=pd.Series([1,2,3],index=list('ABC'))
s1
s2=pd.Series([4,5,6],index=list('BCD'))
s2
s1+s2

df1=pd.DataFrame(np.arange(1,13).reshape(3,4),
                 index=list('abc'),columns=list('ABCD'))
df1       
df1-s1
df2=pd.DataFrame(np.arange(1,13).reshape(4,3),
                 index=list('bcde'),columns=list('CDE'))
df2   
df1*df2
df1
df2
df1.div(df2,fill_value=0)

df0 = pd.DataFrame(np.random.rand(6,4),
                   index=pd.date_range('20160101',periods=6),
                    columns=list('ABCD'))
df0
df0.apply(max,axis=0)
f=lambda x: x.max()-x.min()
df0.apply(f,axis=1)

df1
df2
df3=df1.mul(df2,fill_value=0)
df3
df3.isnull()
df3.notnull()
df3.B[df3.B.notnull()]

df4=pd.DataFrame(np.random.rand(5,4),
                 index=list('abcde'),
                columns=list('ABCD'))
df4.ix['c','A']=np.nan   
df4.ix['b':'d','C']=np.nan         
df4
df4.fillna(0)
df4.fillna(method='ffill')
df4.fillna(method='bfill')
df4.fillna(method='backfill',axis=1) 
df4.fillna(method='pad',limit=2)
df4.fillna('missing', inplace=True)
df4
   
df4.ix['c','A']=np.nan                 
df4.ix['b':'d','C']=np.nan  
df4 

df4.dropna(axis=0)
df4.dropna(axis=1,thresh=3)
df4.dropna(axis=1,how='all')

df5=pd.DataFrame({'c1':['apple'] *3 + ['banana']*3+['apple'], 
                  'c2':['a', 'a', 3, 3, 'b', 'b','a']})
df5
df5.duplicated()
df5.drop_duplicates()
df5.duplicated(['c2'])
df5.drop_duplicates(['c2'])


              
