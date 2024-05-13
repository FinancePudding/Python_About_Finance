#coding:utf-8
#chap13 Descriptive Statistics
import pandas as pd
import os
# os.chdir('E:\\book_data\\part_2')
os.chdir(r'/media/chai/E/迅雷下载/Python Quant Book/part 2')

# /media/chai/E/迅雷下载/Python Quant Book/part 2/part2.py

# returns=pd.read_csv('013\\retdata.csv')
returns=pd.read_csv(r'/media/chai/E/迅雷下载/Python Quant Book/part 2/013/retdata.csv')


gsyh=returns.gsyh
import matplotlib.pyplot as plt
plt.hist(gsyh)
returns.zglt.mean()
returns.pfyh.mean()
returns.zglt.median()
returns.pfyh.median()
returns.zglt.mode()
returns.pfyh.mode()
[returns.zglt.quantile(i) for i in [0.25,0.75]]
[returns.pfyh.quantile(i) for i in [0.25,0.75]]

returns.zglt.max()-returns.zglt.min()
returns.zglt.mad()
returns.zglt.var()
returns.zglt.std()
returns.pfyh.max()-returns.pfyh.min()
returns.pfyh.mad()
returns.pfyh.var()
returns.pfyh.std()

# fund=pd.read_csv('013\\history.csv',sep=';')

fund=pd.read_csv(r'/media/chai/E/迅雷下载/Python Quant Book/part 2/013/history.csv',sep=';')

fund.head()

#chap14 Random Variable
import numpy as np
import pandas as pd

RandomNumber=np.random.choice([1,2,3,4,5],\
                   size=100,replace=True,\
                   p=[0.1,0.1,0.3,0.3,0.2])
pd.Series(RandomNumber).value_counts()
pd.Series(RandomNumber).value_counts()/100

# HSRet300=pd.read_csv('014\\return300.csv')

HSRet300=pd.read_csv(r'/media/chai/E/迅雷下载/Python Quant Book/part 2/014/return300.csv')


HSRet300.head(n=2)

import matplotlib.pyplot as plt
from scipy import stats

density=stats.kde.gaussian_kde(HSRet300.iloc[:,1])

bins=np.arange(-5,5,0.02) #设定分割区间

plt.subplot(211)
plt.plot(bins,density(bins))
plt.title('沪深300收益率序列的概率密度曲线图')

plt.subplot(212)
plt.plot(bins,density(bins).cumsum())
plt.title('沪深300收益率序列的累积分布函数图')

np.random.binomial(100,0.5,20)
np.random.binomial(10,0.5,3)

stats.binom.pmf(20,100,0.5)
stats.binom.pmf(50,100,0.5)

dd=stats.binom.pmf(np.arange(0,21,1),100,0.5)
dd
dd.sum()
stats.binom.cdf(20,100,0.5)

ret=HSRet300.iloc[:,1]
HSRet300.iloc[:,0].head()
ret.head(n=3)

p=len(ret[ret>0])/len(ret)
p

prob=stats.binom.pmf(6,10,p)
prob

Norm=np.random.normal(size=5)
Norm

stats.norm.pdf(Norm)
stats.norm.cdf(Norm)

HS300_RetMean=ret.mean()
HS300_RetMean

HS300_RetVariance=ret.var()
HS300_RetVariance

stats.norm.ppf(0.05,HS300_RetMean,HS300_RetVariance**0.5)

plt.plot(np.arange(0,5,0.002),\
         stats.chi.pdf(np.arange(0,5,0.002),3))
plt.title('Probability Density Plot of Chi-Square Distribution')

x=np.arange(-4,4.004,0.004)
plt.plot(x,stats.norm.pdf(x),label='Normal')
plt.plot(x,stats.t.pdf(x,5),label='df=5')
plt.plot(x,stats.t.pdf(x,30),label='df=30')
plt.legend()

plt.plot(np.arange(0,5,0.002),\
        stats.f.pdf(np.arange(0,5,0.002),4,40))
plt.title('Probability Density Plot of F Distribution')


#correlation
TRD_Index=pd.read_table('014\\TRD_Index.txt',sep='\t')
TRD_Index.head()
SHindex=TRD_Index[TRD_Index.Indexcd==1]
SHindex.head(3)

SZindex=TRD_Index[TRD_Index.Indexcd==399106]
SZindex.head(3)

plt.scatter(SHindex.Retindex,SZindex.Retindex)
plt.title('上证综指与深证成指收益率的散点图')
plt.xlabel('上证综指收益率')
plt.ylabel('深证成指收益率')

SZindex.index=SHindex.index
SZindex.Retindex.corr(SHindex.Retindex)


#chap15   Parameter Estimation and Hypothesis Testing
from scipy import stats
import numpy as np

x=[10.1 ,10 ,9.8 ,10.5 ,9.7,\
   10.1 ,9.9 ,10.2 ,10.3 ,9.9]

stats.t.interval(0.95,len(x)-1,\
              np.mean(x),stats.sem(x))

import pandas as pd
SHindex=pd.read_csv('015\\TRD_Index.csv')
SHindex.head(3)
Retindex=SHindex.Retindex
Retindex.hist()

mu=Retindex.mean()
sigma=Retindex.std()
import matplotlib.pyplot as plt
plt.hist(Retindex,normed=True)
plt.plot(np.arange(-0.06,0.062,0.002),\
   stats.norm.pdf(np.arange(-0.06,0.062,0.002),\
   mu,sigma))
stats.t.interval(0.95,len(Retindex)-1,mu,stats.sem(Retindex))


TRD_Index=pd.read_table('015\\TRD_Index.txt',sep='\t')
SHindex=TRD_Index[TRD_Index.Indexcd==1]
SHRet=SHindex.Retindex
stats.ttest_1samp(SHRet,0)

SZindex=TRD_Index[TRD_Index.Indexcd==399106]
SZRet=SZindex.Retindex
stats.ttest_ind(SHRet,SZRet)

stats.ttest_rel(SHRet,SZRet)

#chap16 ANOVA
import pandas as pd
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols

year_return=pd.read_csv('016\\TRD_Year.csv',\
                        encoding='gbk')
year_return.head()
model=ols('Return ~ C(Industry)',\
          data=year_return.dropna()).fit()
table1 = anova.anova_lm(model)
print(table1)

PSID=pd.read_csv('016\\PSID.csv')
PSID.head(3)
model=ols('earnings ~C(married)+C(educatn)',\
           data=PSID.dropna()).fit()
table2 = anova.anova_lm(model)
print(table2)

model=ols('earnings ~ C(married)*C(educatn)', data=PSID.dropna()).fit()
table3 = anova.anova_lm(model)
print(table3)

#chap17 regression
import pandas as pd
TRD_Index=pd.read_table('017/TRD_Index.txt',sep='\t')
SHindex=TRD_Index[TRD_Index.Indexcd==1]
SZindex=TRD_Index[TRD_Index.Indexcd==399106]
SHRet=SHindex.Retindex
SZRet=SZindex.Retindex
SZRet.index=SHRet.index

import statsmodels.api as sm
model=sm.OLS(SHRet,sm.add_constant(SZRet)).fit()
print(model.summary())
model.fittedvalues[:5]

import matplotlib.pyplot as plt
plt.scatter(model.fittedvalues,model.resid)
plt.xlabel('拟合值')
plt.ylabel('残差')

import scipy.stats as stats
sm.qqplot(model.resid_pearson,\
              stats.norm,line='45')

plt.scatter(model.fittedvalues,\
             model.resid_pearson**0.5)
plt.xlabel('拟合值')
plt.ylabel('标准化残差的平方根')

penn=pd.read_excel('017/Penn World Table.xlsx',2)
penn.head(3)
import numpy as np
model=sm.OLS(np.log(penn.rgdpe),
             sm.add_constant(penn.iloc[:,-6:])).fit()
print(model.summary())

penn.iloc[:,-6:].corr()

model=sm.OLS(np.log(penn.rgdpe),\
             sm.add_constant(penn.iloc[:,-5:-1])).fit()
print(model.summary())