# -*- coding: utf-8 -*-

#1.
import matplotlib.pyplot as plt
x = list(range(1952,2016,4))
y = (29.3,28.8,28.5,28.4,29.4,27.6,27.7,27.7,
	27.8,27.4,27.8,27.1,27.3,27.1,27.0,27.5)
plt.plot(x,y)

import statsmodels.api as sm
model=sm.OLS(y ,sm.add_constant(x)).fit()
print(model.summary())

#2.
import pandas as pd

EU = pd.read_csv('Data/Part2/005/EuStockMarkets.csv')

plt.plot(EU.DAX,EU.FTSE,'.')

plt.xlabel('DAX')

plt.ylabel('FTSE')

#3.
import statsmodels.api as sm

model = sm.OLS(EU.DAX,sm.add_constant(EU.FTSE)).fit()

print(model.summary())

plt.plot(EU.FTSE,EU.DAX,'.',EU.FTSE,model.fittedvalues,'-')

plt.xlabel('FTSE')

plt.ylabel('DAX')

#4.
plt.plot(model.fittedvalues,model.resid,'.')

plt.xlabel('Fitted')

plt.ylabel('Residual') 

import scipy.stats as stats

sm.qqplot(model.resid_pearson,stats.norm,line='45')

plt.plot(model.fittedvalues,model.resid_pearson**0.5,'.')

plt.xlabel('Fitted')

plt.ylabel('Square Root of Standardized Residual')


#5
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

x = [20,25,30,35,40,50,60,65,70,75,80,90]

y = [1.81,1.7,1.65,1.55,1.48,1.4,1.3,1.26,1.24,1.21,1.2,1.18]

plt.plot(x,y,'.')

independent = np.array([x,[i**2 for i in x]]).T

model = sm.OLS(y,sm.add_constant(independent)).fit()

print(model.summary())

model.predict(np.array([1,95,95**2]).T)

#6.
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np

cps = pd.read_csv('Data/Part2/005/CPS1988.csv')

cps.head()

model = smf.ols('np.log(wage)~experience+education+ethnicity',
                data=cps).fit()

print(model.summary())

model.fittedvalues.head()

model2 = smf.ols('np.log(wage)~experience+np.power(experience,2)+education+ethnicity',
                data=cps).fit()

print(model2.summary())








