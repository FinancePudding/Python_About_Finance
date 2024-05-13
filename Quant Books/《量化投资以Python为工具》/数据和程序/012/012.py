# -*- coding: utf-8 -*-
import os
os.chdir('~\\python_quant\\part 1')

import pandas as pd
ChinaBank=pd.read_csv('012\\ChinaBank.csv',index_col='Date')
ChinaBank=ChinaBank.iloc[:,1:]
ChinaBank.head() 
ChinaBank.index=pd.to_datetime(ChinaBank.index)
Close=ChinaBank.Close

import matplotlib.pyplot as plt
plt.plot(Close['2014'])

%matplotlib qt
plt.plot(Close['2014'])
plt.show()

plt.plot([1,1,0,0,-1,0,1,1,-1]) 
plt.rcParams['axes.unicode_minus']=False
plt.plot([1,1,0,0,-1,0,1,1,-1])
plt.ylim(-1.5,1.5)
plt.xticks(range(9),['2015-02-01','2015-02-02','2015-02-03','2015-02-04','2015-02-05',\
'2015-02-06','2015-02-07','2015-02-08','2015-02-09'])

plt.plot([1,1,0,0,-1,0,1,1,-1])
plt.ylim(-1.5,1.5)
plt.xticks(range(9),['2015-02-01','2015-02-02','2015-02-03','2015-02-04','2015-02-05',\
'2015-02-06','2015-02-07','2015-02-08','2015-02-09'],rotation=45)

plt.plot(Close['2014'])
plt.title('中国银行2014年收盘价曲线')

plt.plot(Close['2014'])
plt.title('中国银行2014年收盘价曲线',loc='right') 

plt.plot(Close['2014'])
plt.title('中国银行2014年收盘价曲线')
plt.xlabel('日期')
plt.ylabel('收盘价')

plt.plot(Close['2014'],label='收盘价')
plt.title('中国银行2014年收盘价曲线')
plt.xlabel('日期')
plt.ylabel('收盘价')
plt.grid(True,axis='y')

Open=ChinaBank.Open
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

plt.plot(Close['2015'],'--rD',label='收盘价')
plt.plot(Open['2015'],'--b>',label='开盘价')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('中国银行2015年开盘与收盘价曲线')
plt.grid(True,axis='both')

plt.plot(Close['2015'],'--rD',label='收盘价',linewidth=2)
plt.plot(Open['2015'],'--b>',label='开盘价',lw=10)
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('中国银行2015年开盘与收盘价曲线')
plt.grid(True,axis='both')

Close.describe()
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
a    
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

plt.hist(Close,range=(2.3,5.5),orientation='vertical',cumulative=True,
         histtype='stepfilled',color='red',edgecolor='blue')
plt.title('中国银行收盘价累积分布直方图')

plt.pie(a,labels=('（2,3]','(3,4]','(4,5]','(5,6]'),\
        colors=('b', 'g', 'r', 'c'),shadow=True) 
plt.title('中国银行收盘价分布饼图')

import numpy as np
prcData=ChinaBank.iloc[:,:4]
data=np.array(prcData)
plt.boxplot(data,labels=('Open','High','Low','Close'))
plt.title('中国银行股价箱形图')

fig=plt.figure()
ax1=fig.add_axes([0.1, 0.1, 0.3, 0.3])
ax2=fig.add_axes([0.5, 0.5, 0.4, 0.4])
ax1.plot(Close[:10])
ax2.plot(Open[:10])
ax1.set_title('前十个交易日收盘价')
ax1.set_xlabel('日期')
ax1.set_xticklabels(Close.index[:10],rotation=25)
ax1.set_ylabel('收盘价')
ax1.set_ylim(2.4,2.65)
ax2.set_title('前十个交易日开盘价')
ax2.set_xlabel('日期') 
ax2.set_xticklabels(Open.index[:10],rotation=25)
ax2.set_ylabel('开盘价')
ax2.set_ylim(2.4,2.65)

ax1=plt.subplot(221)
ax2=plt.subplot(222)
ax3=plt.subplot(223)
ax4=plt.subplot(224)

Close15=Close['2015']
ax1=plt.subplot(211)
ax1.plot(Close15,color='k')
ax1.set_ylabel('收盘价')
ax1.set_title('中国银行2015年收盘价曲线图')

Volume15=ChinaBank.Volume['2015']
Open15=Open['2015']
ax2=plt.subplot(212)
left1=Volume15.index[Close15>=Open15]
hight1=Volume15[left1]
ax2.bar(left1,hight1,color='r')
left2=Volume15.index[Close15<Open15]
hight2=Volume15[left2]
ax2.bar(left2,hight2,color='g')

ax2.set_ylabel('成交量')
ax2.set_title('中国银行2015年成交量柱状图')

#提取价格数据
High15=ChinaBank.High['2015']
Low15=ChinaBank.Low['2015']
#创建axes对象
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

#绘制四条曲线
ax.plot(Close15,label='收盘价')
ax.plot(Open15,'--*',label='开盘价')
ax.plot(High15,'-+',label='最高价')
ax.plot(Open15,'-.>',label='最低价')

#在axes对象中增加文本对象
ax.set_title('中国银行2015年价格图')
ax.set_ylabel('价格')
ax.legend(loc='best')


