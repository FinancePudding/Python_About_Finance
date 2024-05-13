
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import statsmodels.formula.api as smf
from statsmodels.api import add_constant

#1.
wanke = web.DataReader('000002.SZ','yahoo',
                      dt.datetime(2015,1,1),dt.datetime(2015,12,31))

gldc = web.DataReader('600185.SS','yahoo',
                      dt.datetime(2015,1,1),dt.datetime(2015,12,31))

price = pd.concat([wanke.Close,gldc.Close],1)

price.columns=['wanke','geli']

ret = (price-price.shift(1)) / price.shift(1)

model = smf.ols('wanke~geli',data=ret).fit()

print(model.summary())

#5.

zyhy = pd.read_table('Data/Part3/004/problem21.txt', 
  sep='\t',usecols=['zyhy','Date'],index_col='Date')                     
zyhy.index=pd.to_datetime(zyhy.index)
                     
ret = (zyhy-zyhy.shift(1))/zyhy.shift(1)

ThreeFactors = pd.read_table('Data/Part3/004/ThreeFactors.txt', 
  sep='\t',index_col='TradingDate')                            
ThreeFactors.index=pd.to_datetime(ThreeFactors.index)
ThrFac=ThreeFactors['2014']
ThrFac=ThrFac.iloc[:,[2,4,6]]
dat=pd.concat([ret,ThrFac],1)

model = smf.ols('zyhy~RiskPremium2+SMB2+HML2',data=dat).fit()
print(model.summary())

#6.
zhongxin = pd.read_table('Data/Part3/004/problem21.txt', 
  sep='\t',usecols=['zhongxin','Date'],index_col='Date')

zhongxin.index=pd.to_datetime(zhongxin.index)
                     
ret = (zhongxin-zhongxin.shift(1))/zhongxin.shift(1)

ThreeFactors = pd.read_table('Data/Part3/004/ThreeFactors.txt',
 sep='\t',index_col='TradingDate')
                             
ThreeFactors.index=pd.to_datetime(ThreeFactors.index)

ThrFac=ThreeFactors['2014']
ThrFac=ThrFac.iloc[:,[2,4,6]]
dat=pd.concat([ret,ThrFac],1)

model = smf.ols('zhongxin~RiskPremium2',data=dat).fit()
print(model.summary())


model2 = smf.ols('zhongxin~RiskPremium2+SMB2+HML2',data=dat).fit()
print(model2.summary())


ThrFac=ThreeFactors['2015-01']
preCAPM = model.predict(add_constant(ThrFac.RiskPremium2),
  transform=False)
preFactors = model2.predict(add_constant(ThrFac[['RiskPremium2','SMB2','HML2']]),
  transform = False)


#7.
import pandas as pd

codes = pd.read_csv('Data/Part3/004/codes.csv', header=None,dtype=str)

ThreeFactors = pd.read_table('Data/Part3/004/ThreeFactors.txt', sep='\t',index_col='TradingDate')
                             
ThreeFactors.index=pd.to_datetime(ThreeFactors.index)

ThrFac=ThreeFactors['2014']

ThrFac=ThrFac.iloc[:,[2,4,6]]

def create_func(model):
    def cal_alpha(code,model_name=model):
        price = web.DataReader(code,'yahoo',
                          dt.datetime(2014,1,1),dt.datetime(2014,12,31)).Close
                         
        ret = (price-price.shift(1))/price.shift(1)
        
        ret.name = 'ret'
        
        dat=pd.concat([ret,ThrFac],1)
        
        if model_name=='CAPM':
            model = smf.ols('ret~RiskPremium2',data=dat).fit()
        elif model_name=='factors':
            model = smf.ols('ret~RiskPremium2+SMB2+HML2',data=dat).fit()
        
        return(model.params[0])
    return(cal_alpha)
    
alpha_CAPM=list(map(create_func('CAPM'),codes[0].values))
alpha_CAPM2=pd.Series(alpha_CAPM).sort(ascending=False,inplace=False)
alpha_CAPM2[:3] 

alpha_factors=list(map(create_func('factors'),codes[0]))
alpha_factors2 = pd.Series(alpha_factors).sort(ascending=False,inplace=False)
alpha_factors2[:3] 