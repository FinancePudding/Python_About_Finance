import pandas as pd
ChinaBank=pd.read_csv('E:\\book_data\\part 1\\012\\ChinaBank.csv',index_col='Date')

ChinaBank=ChinaBank.iloc[:,1:]

ChinaBank.head() 

ChinaBank.index=pd.to_datetime(ChinaBank.index)
Close=ChinaBank.Close
Open=ChinaBank.Open



%matplotlib qt
plt.rcParams['font.sans-serif']=['SimHei']

import matplotlib.pyplot as plt

plt.plot(Close['2014'],label='收盘价')
plt.plot(Open['2014'],label='开盘价')
plt.legend() 

plt.plot(Close['2014'],label='收盘价',linestyle='solid')
plt.plot(Open['2014'],label='开盘价',ls='-.')
plt.legend()
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('中国银行2014年开盘与收盘价曲线')
plt.grid(True,axis='y')

plt.plot(Close['2014'],c='r',label='收盘价')
plt.plot(Open['2014'],c='b',ls='--',label='开盘价')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('中国银行2014年开盘与收盘价曲线')
plt.grid(True,axis='both')

plt.plot(Close['2015'],marker='o',label='收盘价')
plt.plot(Open['2015'],marker='*',label='开盘价')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('中国银行2015年开盘与收盘价曲线')
plt.grid(True,axis='both')



plt.title('中国银行2014年收盘价曲线')
plt.xlabel('日期')
plt.ylabel('收盘价')
plt.grid(True,axis='both')

plt.plot([1,1,0,0,-1,0,1,1,-1]) 
plt.ylim(-1.5,1.5)
plt.xticks(range(9),\
            ['2015-02-01','2015-02-02',\
            '2015-02-03','2015-02-04',\
            '2015-02-05','2015-02-06',\
            '2015-02-07','2015-02-08','2015-02-09']) 

plt.title('中国银行2014年收盘价曲线',loc='right')
plt.show()

a=[0,0,0,0]
for i in Close:
    if (i>2)&(i<=3):
        a[0]+=1
    elif (i>3)&(i<=4):
        a[1]+=1 
    elif (i>4)&(i<=5):
        a[2]+=1
    else:
        a[3]+=1
        
plt.bar([2,3,4,5],a)
plt.bar(left=[2,3,4,5],height=a,width=1.0,bottom=2.0)
plt.title('中国银行收盘价分布柱状图')

plt.bar(left=[2,3,4,5],height=a,width=1.0,bottom=2.0,color='red',edgecolor='k')
plt.title('中国银行收盘价分布柱状图')

plt.barh([2,3,4,5],a,height=1.0,color='red',edgecolor='k')
plt.title('中国银行收盘价分布柱状图')

plt.hist(Close,bins=12)
plt.title('中国银行收盘价分布直方图')

plt.hist(Close,range=(2.3,5.5),orientation='horizontal',color='red',edgecolor='blue')
plt.title('中国银行收盘价分布直方图')

plt.pie(a,labels=('（2,3]','(3,4]','(4,5]','(5,6]'),\
        colors=('b', 'g', 'r', 'c'),shadow=True)
plt.title('中国银行收盘价分布饼图')