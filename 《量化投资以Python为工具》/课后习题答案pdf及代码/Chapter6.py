# -*- coding: utf-8 -*-

#1、
def is_odd(i):
    if type(i) == int:
        return(i if i%2==1 else 0)
    else:
        print('ERROR：Please input an integer.')
is_odd(7)

#2、
import random
a=[random.normalvariate(0,1) for i in range(5)]
for j in a:
    if j>=0:
        print('Big')
    else:
        print('Small')
        
#3、
I = []
for i in range(5):
    row = [0 for j in range(5)]
    row[i] = 1
    I.append(row)
I 
  
#4、
for i in (-1,0,1,2,39):
    print(i in range(1,5))
    
#5、
Hilbert = []
for i in range(4):
    Hilbert.append([])
    for j in range(4):
        Hilbert[i].append(1/(i+j+1))
Hilbert
