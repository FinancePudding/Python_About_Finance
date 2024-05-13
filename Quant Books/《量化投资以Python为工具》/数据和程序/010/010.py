# Section 10.1.1
import numpy as np
array1=np.array(range(6))
print(array1)
array1.shape
array1.shape=2,3
print(array1)

array2=array1.reshape(3,2)
print(array2)
array2.shape
array1.shape
array1[1,2]=88
print(array1)
print(array2)

array3=np.array([[1,2,3], [4,5,6], [7,8,9]])
print(array3)
array3.shape

array4=np.arange(13,1,-1)
print(array4)
array4.shape=2,2,3
print(array4)

array5=array4.reshape(3,2,2)
array5

array6=np.linspace(1,12,12)
print(array6)
array6.dtype

array7=np.linspace(1,12,12,dtype=int)
print(array7)

a = np.zeros( (4,5) ) # 利用 zeros() 函 数 生 成 数 组
a
a.dtype

np.ones((2,5,4),dtype=np.int16)

np.empty( (3,2) )

# Section 10.1.2
a1=np.linspace(1,26,6,dtype=int)
a1
a1[3]
a1[1:3]
a1[:5]
a1[2:]
a1[-1]
a1[-3]
a1[:-1]
a1[2:-1]

a2=a1[0:3:1]
a2
a1[0]=19
a2[0]



a1[[0,1,4]]
a3=a1[[0,3,2]]
a3
a1[0]=23
a3[0]

na1=np.array(np.arange(24),dtype=int).reshape(4,6)
print(na1)
na1[:2,1:]
na1[[2,3],[2,4]]
na1[2:,[2,4]]
na2=na1.reshape(2,3,4)
na2
na2[(1,1,2)]
na2[1,1,2]
na2[[1,1,0],[0,1,2],[2,3,1]]
na2[(1,1,1),(0,1,2),(2,3,1)]

# Section 10.1.3
ar1=np.array(np.arange(5))
ar1
np.add(ar1,4)
ar2=np.array([2,3,4,5,6])
ar2
ar1+ar2
np.add(ar1,ar2)
np.add(ar1,ar2,ar1)
ar1

a = np.array( [10,20,30,50,60] )
b = np.arange( 5 )
b
c=a-b
c
b**2
10*np.cos(a)
a<40