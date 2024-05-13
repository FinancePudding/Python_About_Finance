'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 3\\021')
'''

import pandas as pd
stock=pd.read_table('stock.txt',sep='\t',index_col='Trddt')
stock.head(n=3)
HXBank = stock[stock.Stkcd==600015]
HXBank.head(n=3)
HXBank.index=pd.to_datetime(HXBank.index)
HXRet=HXBank.Dretwd
HXRet.name='HXRet'
HXRet.head()
HXRet.tail()
HXRet.plot()
ThreeFactors=pd.read_table('ThreeFactors.txt',sep='\t',
                           index_col='TradingDate')
ThreeFactors.head(n=3)
ThreeFactors.index=pd.to_datetime(ThreeFactors.index)
ThrFac=ThreeFactors['2014-01-02':]
ThrFac=ThrFac.iloc[:,[2,4,6]]
ThrFac.head()
HXThrFac=pd.merge(pd.DataFrame(HXRet),pd.DataFrame(ThrFac),
                  left_index=True,right_index=True)
HXThrFac.head(n=3)
HXThrFac.tail(n=3)
import matplotlib.pyplot as plt
plt.subplot(2,2,1)
plt.scatter(HXThrFac.HXRet,HXThrFac.RiskPremium2)
plt.subplot(2,2,2)
plt.scatter(HXThrFac.HXRet,HXThrFac.SMB2)
plt.subplot(2,2,3)
plt.scatter(HXThrFac.HXRet,HXThrFac.HML2)

import statsmodels.api as sm
regThrFac=sm.OLS(HXThrFac.HXRet,sm.add_constant(HXThrFac.iloc[:,1:4]))
result=regThrFac.fit()
result.summary()

result.params