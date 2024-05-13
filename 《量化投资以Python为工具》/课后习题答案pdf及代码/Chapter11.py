# -*- coding: utf-8 -*-

import numpy as np

#1.
odds = [i+1 for i in range(20) if (i+1)%2==1]
odds = np.array(odds)

#2.
three = tuple([i+1 for i in range(40) if (i+1)%3==0])
three = np.array(three)

#3.
same_number = odds[np.in1d(odds,three)]
#method1
print(same_number[:round(len(same_number/2))])
#method2
for i in range(round(len(same_number/2))):
    print(same_number[i])

#4.    
np.random.uniform(0,10,10)

#5.
even = np.arange(2,22,2)

#6.
even[-5:]
even[len(even)-5:]

#7.
import pandas as pd
data = pd.DataFrame({'id':['a','b','c','d','e','f'],'name':
    ['Alice','Bob','Charlie','David','Esther','Fanny'],'age':
        [34,36,30,29,32,36]})
       
data.T.ix[2]
new = pd.DataFrame({'id':['g'],'name':['John'],'age':[19]})
data = data.append(new)
data.index = data.age
data
data = data.drop(30)
data

