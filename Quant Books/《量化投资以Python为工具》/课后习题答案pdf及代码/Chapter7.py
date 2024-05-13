# -*- coding: utf-8 -*-

#1、
x=[1,2 ,3]
def permutation(x):
    x[0],x[-1]=x[-1],x[0]
    return(x)
y=permutation(x)
y is x


#2、
def sum_lists(x,y):
    return([x[i]+y[i] for i in range(len(x))])

#3、
def sum2(*lists):
    if len(lists)==2:
        return(sum_lists(lists[0],lists[1]))
    else:
        return(sum_lists(lists[0],sum2(*lists[1:])))
        
#4、
def fibo(n):
    if(n<3):
        a=1
    else:
        a=fibo(n-1)+fibo(n-2)
    return(a)
def seqfibo(n):
    for i in range(1,n+1):
        print(fibo(i))
seqfibo(5)
        
#5、
def multi_abs(*numbers):
    return(list(map(abs,numbers)))
multi_abs(-5,55,-6,0,-7)
    
#6、
def count_positive(returns):
    return(sum(map(lambda x: x>0,returns)))
ret=[-0.4,0.5,-0.34,0.45,0.50]
count_positive(ret)