
#%%
#a is a turple
a=[2,3,5,6,15]

#b is a turple
b=[2,5,9,8,10]

#merge elements in a and b
c=a+b
print(c)

#%%
#sum elements in a and b
d=list()  
for i in range(5):
    j=a[i]+b[i]
    d.append(j)
print(d)

