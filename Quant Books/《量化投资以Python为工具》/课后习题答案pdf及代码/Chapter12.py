# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#1.
Money = pd.read_csv('Data/Part1/012/Money.csv',
                    index_col='date')
                    
axis1 = plt.subplot()
axis1.plot(Money.index,Money.m,'-')
plt.title('Money Supply of Canada')
plt.xlabel('Year')
axis2 = axis1.twinx()
axis2.plot(Money.y,'-')
plt.show()

#2.
Journals = pd.read_csv('Data/Part1/012/Journals.csv')
plt.scatter(Journals.citestot,Journals.libprice)
plt.title('Price vs Citations')
plt.xlabel('Citations')
plt.ylabel('Price')
plt.show()

#3.
mtcars = pd.read_csv('Data/Part1/012/mtcars.csv')
types=np.array([0.2,0.6])
number = mtcars.groupby(['gear','vs'])['vs'].agg(len)
plt.bar(types,number.ix[3],width=0.3,label='gear=3')
plt.bar(types,number.ix[4],width=0.3,
	bottom=number.ix[3],color='r',
	label='gear=4')
plt.bar(types,number.ix[5],width=0.3,
	bottom=number.ix[3]+number.ix[4],
	color='y',label='gear=5')
plt.xlim([0,1])
plt.ylim([0,25])
plt.legend()
plt.xticks(types+0.3/2,[0,1])
plt.show()

#4.
Arthritis = pd.read_csv('Data/Part1/012/Arthritis.csv')
plt.hist(Arthritis.Age)
plt.xlabel('Age')
plt.title('Histogram of Age')
plt.show()

#5.
norm1 = np.random.normal(0,1,100)
norm2 = np.random.normal(0,2,100)
norm3 = np.random.normal(0,3,100)
norm4 = np.random.normal(0,4,100)
plt.boxplot([norm1,norm2,norm3,norm4])
plt.xlabel('Standard Deviation')
plt.title('Normal Distributions with Different Standard Deviation')
plt.show()

#6.
norm1 = np.random.normal(0,1,100)
norm2 = np.random.normal(0,2,100)
norm3 = np.random.normal(0,3,100)
norm4 = np.random.normal(0,4,100)
figure,axes = plt.subplots(2,2)
axes[0,0].scatter(range(100),norm1)
axes[0,1].scatter(range(100),norm2)
axes[1,0].scatter(range(100),norm3)
axes[1,1].scatter(range(100),norm4)
plt.show()

#7.
tan_value = np.tan(np.linspace(0,2*np.pi,10001))[np.newaxis,:]
tan_value = np.concatenate((np.linspace(0,2*np.pi,10001)[np.newaxis,:],
                            tan_value),0)
tan_value=np.where(tan_value>200,200,
                   np.where(tan_value<-200,-200,tan_value))
plt.plot(tan_value[0],tan_value[1],'o')
plt.show()