# Section 6.1
a=[1,2,3]

id(a)

b=a

id(b)

b[1]=25

id(a)

id(b)

a

b

b[1]=2

a

b

c=[1,2,3]

id(c)

c is a

c==a

c[2]=88

c

a

b

# Section 6.1.2
x=y=z=25678
x
y
z

x1=y1=z1=[2,5,6,7,8]

x1

(x1 is y1) and (y1 is z1) and (x1 is z1)

# Section 6.1.3
x2,y2,z2=2,5,6

x2

y2

z2

x3=2,5,6

# Section 6.1.4
a=6
a*=3
a

b=17
b-=6
b

c=21
c%=3
c

# Section 6.2
a=6
b=4
if a>b:
    print(' 变量 a 的 值 大 于 变 量 b 的值 ')
else:
    print(' 变量 b 的 值 大 于 变 量 a 的值 ')

if a>5 and b>5:
    a+=6
else:
    b+=6

a

b

grade=95
if grade >=90:
    print("Excellent job")
elif all([grade >70,grade <90]):
    print("good job")
else:
    print("It's uncommon")
    
a=6
b=4
' 变量 a 的 值 大 于 变 量 b 的值 ' if a>b else ' 变量 b 的 值 大 于 变 量 a 的值 '

a=4**3 if {} else '123'

a

# Section 6.3
for i in [2,3,5,6,7]:
    print(i)
    
a=list()
for i in 'python':
    a.append(i+'python')
    print(a)
    
a=list()
for i in 'python':
    a.append(i+'python')
print(a)

a=[i+'python' for i in 'python']
a

list1=[2,10,34,3,10,20,10]
[i for i in range(len(list1)) if list1[i]==10]

# Section 6.3.2
a=0
while a<4:
    a=a+1
    print(a+26)
print(a)

# Section 6.3.3
x=['a','b','c']
y=[2,3]
z=[]
for i in x:
    for j in y:
        z.append([i,j])
print(z)

[[i,j] for i in x for j in y]

# Section 6.3.4
st1=['a','b','python','c','d']
for i in st1:
    print(i)
    if i=='python':
        break # 跳出 for 循环
        
for i in st1:
    print(i)
    if i=='python':
        break # 跳出 for 循环
    print('hello') #和 print(i) 语 句 缩 进 格 式 相 同 ， 属 于 同 级 关 系
    
for i in st1:
    print(i)
    if i=='python':
        break # 跳出 for 循环
print('hello') # 缩 进 和 for 所 在 行 相 同 ， 在 for 循 环 结 束 以 后 总 会 执 行 该 代 码

for i in st1:
    if i=='python':
        continue # 停 止 执 行 当 前 循 环 语 句 中 的 内 容 ， 并 进 入 下 一 次 循 环
    print(i) #在 for 循 环 语 句 内 部
print('hello') #和 print(i) 语 句 缩 进 格 式 相 同 ， 属 于 同 级 关 系

for i in st1:
    if i=='python':
        continue # 停 止 执 行 当 前 循 环 语 句 中 的 内 容 ， 并 进 入 下 一 次 循 环
    print(i) #在 for 循 环 语 句 内 部
    print('hello') #在 for 循 环 内 部
    
for i in st1:
    print(i) 
    if i=='python':
        continue     
print('hello') #在 for 循 环 内 部

for i in st1:
    if i=='python':
        continue
        print(i) #在 for 循 环 的 if 语 句 内 部 ， 位于 continue 下方 ， 永 远 不 会 被 执 行
print('hello')

for i in range(5):
    if i>3:
        pass
    print([i,i+1])
    