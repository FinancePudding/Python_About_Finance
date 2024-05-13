# -*- coding: utf-8 -*-
#1、
3+4
3.4*4
3//4
id(['a',3,True ,'scd'][1])== id(3)
3==4 in [1,'345' ,3+4j,4 in [1 ,2 ,3]]
(3==4*4.5%2 is 0) in [3,4,'Tom','c' in 'comic ']

#3、
a=[1,2,3]
c=2
sum([i>c for i in a])==len(a)

#4、
import random
a=[random.normalvariate(0,1) for i in range(20)]
a.sort()
a[0]
a[-1]
sum(a)