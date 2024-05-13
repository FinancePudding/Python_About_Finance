# -*- coding: utf-8 -*-


#1、
type((1,3,5,7))
type('pi')
type(5>6)
type({'High':7.45,'Low':7.30})
type(['Hello world ' ,3,4,('a','b'),True])


#2、
(3+4j)*(4+3j)
3/4
True *3
0.003-0.0022222

#3、
a = [1, 2, 3]
b=a
b
id(a)==id(b)
b[0]=3
a
id(a)==id(b)

True
[3,2,3]
True

#4、
a=tuple(range(1,11))
b=tuple((i+1 for i in range(20) if (i+1)%2==1))
c=[5*i for i in range(11)]
d=[];
for i in range(1,6):
	j=0
	while(j<3):
		d.append(i)
		j+=1
d

e=set({'NASDAQ','Dowjones','DAX','FTSE'})

#5、
tuple('abc')
list('abc')
set('abc')

#6、
characters={'A':ord('A'),'b':ord('b'),'\n':ord('\n')}
characters