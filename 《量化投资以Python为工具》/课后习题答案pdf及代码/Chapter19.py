import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import ffn
from scipy import linalg
class MeanVariance:
    def __init__(self,returns):
        self.returns=returns
    def minVar(self,goalRet):
        covs=np.array(self.returns.cov())
        means=np.array(self.returns.mean())
        L1=np.append(np.append(covs.swapaxes(0,1),[means],0),
                     [np.ones(len(means))],0).swapaxes(0,1)
        L2=list(np.ones(len(means)))
        L2.extend([0,0])
        L3=list(means)
        L3.extend([0,0])
        L4=np.array([L2,L3])
        L=np.append(L1,L4,0)
        results=linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
        return(np.array([list(self.returns.columns),results[:-2]]))
    def frontierCurve(self):
        goals=[x/500000 for x in range(-100,4000)]
        variances=list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float)),goals))
        plt.plot(variances,goals)
    def meanRet(self,fracs):
        meanRisky=ffn.to_returns(self.returns).mean()
        assert len(meanRisky)==len(fracs), 'Length of fractions must be equal to number of assets'
        return(np.sum(np.multiply(meanRisky,np.array(fracs))))
    def calVar(self,fracs):
        return(np.dot(np.dot(fracs,self.returns.cov()),fracs))



#5. 
sclq = web.DataReader('600039.SS','yahoo',
            dt.datetime(2009,1,2),dt.datetime(2012,12,31)).Close
sclqRet=((sclq-sclq.shift(1))/sclq.shift(1))
sclqRet.name='sclq'

hsly = web.DataReader('600054.SS','yahoo',
           dt.datetime(2009,1,2),dt.datetime(2012,12,31)).Close
hslyRet=((hsly-hsly.shift(1))/hsly.shift(1))
hslyRet.name='hsly'

wldc = web.DataReader('600173.SS','yahoo',
            dt.datetime(2009,1,2),dt.datetime(2012,12,31)).Close
wldcRet=((wldc-wldc.shift(1))/wldc.shift(1))
wldcRet.name='wldc'

ghny = web.DataReader('600256.SS','yahoo',
            dt.datetime(2009,1,2),dt.datetime(2012,12,31)).Close
ghnyRet=((ghny-ghny.shift(1))/ghny.shift(1))
ghnyRet.name='ghny'

zhjt = web.DataReader('600252.SS','yahoo',
           dt.datetime(2009,1,2),dt.datetime(2012,12,31)).Close
zhjtRet=((zhjt-zhjt.shift(1))/zhjt.shift(1))
zhjtRet.name='zhjt'

fiveStocks=pd.concat([sclqRet,hslyRet,wldcRet,ghnyRet,zhjtRet],1)
fiveStocks=fiveStocks.dropna()

minVar=MeanVariance(fiveStocks)
minVar.frontierCurve() 

#6.
goal_return=0.05
portfolio_weight=minVar.minVar(goal_return)
portfolio_weight

#8.
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import ffn
from scipy import linalg

def blacklitterman(returns,tau, P, Q):
  mu=returns.mean()
  sigma=returns.cov()
  pi1=mu
  ts = tau * sigma
  Omega = np.dot(np.dot(P,ts),P.T) * np.eye(Q.shape[0])
  middle = linalg.inv(np.dot(np.dot(P,ts),P.T) + Omega)  
  er = np.expand_dims(pi1,axis=0).T + np.dot(np.dot(np.dot(ts,P.T),middle),
                      (Q - np.expand_dims(np.dot(P,pi1.T),axis=1)))
  posteriorSigma = sigma + ts - np.dot(ts.dot(P.T).dot(middle).dot(P),ts)
  return [er, posteriorSigma]

def blminVar(blres,goalRet):
    covs=np.array(blres[1])
    means=np.array(blres[0])
    L1=np.append(np.append((covs.swapaxes(0,1)),[means.flatten()],0),
                           [np.ones(len(means))],0).swapaxes(0,1)
    L2=list(np.ones(len(means)))
    L2.extend([0,0])
    L3=list(means)
    L3.extend([0,0])
    L4=np.array([L2,L3])
    L=np.append(L1,L4,0)
    results=linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
    return(pd.DataFrame(results[:-2],
                        index=blres[1].columns,columns=['p_weight']))

pick1 = np.array([1,0,0,0])
pick2 = np.array([0,-1,0,1])
pick3 = np.array([1,0,-1,0])
P = np.array([pick1,pick2,pick3])
Q=np.array([[0.06],[0.02],[0.03]])

lcxx = web.DataReader('000977.SZ','yahoo',
            dt.datetime(2012,1,2),dt.datetime(2014,12,31)).Close
lcxxRet=((lcxx-lcxx.shift(1))/lcxx.shift(1))
lcxxRet.name='lcxx'

pfyh = web.DataReader('600000.SS','yahoo',
            dt.datetime(2012,1,2),dt.datetime(2014,12,31)).Close
pfyhRet=((pfyh-pfyh.shift(1))/pfyh.shift(1))
pfyhRet.name='pfyh'

htzq = web.DataReader('601688.SS','yahoo',
            dt.datetime(2012,1,2),dt.datetime(2014,12,31)).Close
htzqRet=((htzq-htzq.shift(1))/htzq.shift(1))
htzqRet.name='htzq'

zqb = web.DataReader('300052.SZ','yahoo',
            dt.datetime(2012,1,2),dt.datetime(2014,12,31)).Close
zqbRet=((zqb-zqb.shift(1))/zqb.shift(1))
zqbRet.name='zqb'

Stocks=pd.concat([lcxxRet,pfyhRet,htzqRet,zqbRet],1)
Stocks=Stocks.dropna()
        
res=blacklitterman(Stocks,0.1, P, Q)
blminVar(res,0.75/252)

####
#      p_weight
#lcxx -0.015149
#pfyh  0.810286
#htzq  0.082629
#zqb   0.122235
