# 8
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import statsmodels.formula.api as smf

rf=1.036**(1/360)-1

nyyh = web.DataReader('601288.SS','yahoo',
                      dt.datetime(2014,1,1),dt.datetime(2014,12,31))                     
returns = (nyyh.Close-nyyh.Close.shift(1))/nyyh.Close.shift(1)


indexcd=pd.read_csv('Data/Part3/003/TRD_Index.csv',index_col='Trddt')
mktcd=indexcd[indexcd.Indexcd==902]
mktret=pd.Series(mktcd.Retindex.values,index=pd.to_datetime(mktcd.index))
mktret.name='mktret'
mktret=mktret['2014-01-02':'2014']

dat = pd.concat([mktret,returns],1)
dat = dat - rf

model = smf.ols('Close~mktret',data=dat).fit()

print(model.summary())

# 9.
from statsmodels.api import add_constant

rf=1.036**(1/360)-1

lsw = web.DataReader('300104.SZ','yahoo',
                      dt.datetime(2014,1,1),dt.datetime(2014,12,31))
                      
returns = (lsw.Close-lsw.Close.shift(1))/lsw.Close.shift(1)

indexcd=pd.read_csv('Data/Part3/003/TRD_Index.csv', index_col='Trddt')
mktcd=indexcd[indexcd.Indexcd==902]
mktret=pd.Series(mktcd.Retindex.values,index=pd.to_datetime(mktcd.index))
mktret.name='mktret'
mktret=mktret['2014-01-02':'2014']

dat = pd.concat([mktret,returns],1)
dat = dat - rf

model = smf.ols('Close~mktret',data=dat).fit()
print(model.summary())


ret_2015=pd.Series(mktcd.Retindex.values,index=pd.to_datetime(mktcd.index))['2015-01']
ret_2015.name='mktret'
ret_2015 = (ret_2015 - rf)
prediction = model.predict(add_constant(ret_2015),transform=False)


import pypyodbc
import pandas as pd
import datetime as dt
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.api import add_constant

for line in open('Data/Part3/003/industryCodes.txt', encoding='utf-8'):
	listData=line.split(',')
	fileName=listData[0]
	listData[-1]=listData[-1][:6]
	if fileName=='银行':
		break

indexcd=pd.read_table('Data/Part3/003/TRD_Index.txt', sep='\t',index_col='Trddt')
mktcd=indexcd[indexcd.Indexcd==902]
mktret=pd.Series(mktcd.Retindex.values,index=pd.to_datetime(mktcd.index))
mktret.name='mktret'
def GetStockAlpha(symbol,mktret):
	if symbol[0]=='0':
		i=0
		while (symbol[i]=='0'):
			i+=1
		symbol=symbol[i:]
	accessName='Data/Part3/003/Stock.accdb'
 #先提前安装Microsoft Access Database Engine
 #下载地址为https://www.microsoft.com/zh-tw/download/details.aspx?id=13255
	conn = pypyodbc.connect(r'Driver=Microsoft Access Driver (*.mdb, *.accdb);DBQ=%s;' %accessName )
	cursor = conn.cursor()
	cursor.execute('select Stkcd, Trddt, Clsprc from stock where Stkcd=%s;' %symbol )
	data=cursor.fetchall()
	prices=[]
	dates=[]
	for entry in data:
		prices.append(entry[-1])
		time=str(entry[1])
		date=pd.to_datetime(time)
		dates.append(date)
	price=pd.Series(np.array(prices),index=dates)['2013']
	returns = (price-price.shift(1))/price.shift(1)
	returns.name='stock'
 
	rf=1.036**(1/360)-1
	dat = pd.concat([mktret['2013-01-06':'2013'],returns['2013-01-06':'2013']],1)
	dat = dat - rf
	model = smf.ols('stock~mktret',data=dat).fit()
	return(model.params[0])
 
alphas={}
for symbol in listData[1:]:
	try:
		alphas[symbol]=GetStockAlpha(symbol,mktret)
	except Exception as e:
		print (Exception,":",e)

selectAlpha=[('-00',-100000),('-00',-100000),('-00',-100000)]
for symbol in alphas.keys():
	if alphas[symbol]>selectAlpha[0][1]:
		selectAlpha[0]=(symbol,alphas[symbol])
		selectAlpha.sort(key=lambda d:d[1])
selectAlpha		






		
	