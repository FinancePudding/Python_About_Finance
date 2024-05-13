import pandas as pd
import matplotlib.pyplot as plt

#5.
CRSPday=pd.read_csv('Data/Part4/002/CRSPday.csv')
ibm=CRSPday.ibm
ibm.plot()

from statsmodels.graphics.tsaplots import *
plot_acf(ibm,lags=20)

from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(ibm)[1:13],len(ibm))
LjungBox[1][-1] 

#6.
ge=CRSPday.iloc[:,3]
ge.plot() 

plot_acf(ge,lags=20)

LjungBox=stattools.q_stat(stattools.acf(ge)[1:2],len(ge))
LjungBox[1][-1]

LjungBox=stattools.q_stat(stattools.acf(ge)[1:9],len(ge))
LjungBox[1][-1]

#7.
SP500=pd.read_csv('Data/Part4/002/SP500.csv')
r500=SP500.r500
r500.plot() 

plot_acf(r500,lags=20)
plot_pacf(r500,lags=20)

from arch.unitroot import ADF
adf=ADF(r500,lags=3)
print(adf.summary().as_text())