# Section 3.1
7

x = 7

x

x = 8.1

x

# Section 3.2
VariableName = 3
print(VariableName)

变量名称 = 3
print(变量名称)

変数の名前 = 4
print(変数の名前)

dir()

a = 6

A = 4

a-A

print(a,A)

# Section 3.3
# Section 3.3.1
a = 9

type(a)

0b100

0o77

0x123

# Section 3.3.2
b = 9.0

b

type(b)

0.1 + 0.1 + 0.1

# Section 3.3.3
False

True

False == 0

True == 1

True + 3

False + 3

bool({})

bool("False")

bool(False)

bool(2)

bool(1)

bool(None)

# Section 3.3.4
ComplexNumber1=complex(3,6)
ComplexNumber1

# Note: Code in the next line will return an error message
3+6i

3+6j

4+7J

ComplexNumber2=4+6j

type(ComplexNumber2)

# Section 3.4
Job = 'Quant'

type(Job)

Job[0]

Job[1]

# Section 3.5
L0 = [1, 2, 3]
L0[2]

L1 = ['Stock A','Stock B', 'Stock C']
L1[0]

L1[3]

L2 = [10, 'Price', ['Industry 1','Industry 2']]
L2

L2[2]

L2[2][1]

# Section 3.6
x = 7
y = 7

print(id(x))
print(id(y))

z = x

x

z

print(id(z))

z = 8

x

id(x)

id(z)

x = 9

id(x)

x1 = 7
id(x1)

s1 = 'Hello World'
id(s1)

s1 = 'Hi World'
id(s1)

s1[0]

s1[0] = 'W'

L2[0] = 20

L2

L4 = L1

L4

L4[2] = 'Stock D'

L1

# Section 3.7
M = ('Market', 3.0, [10, 20, 30])

t1 = ('Single')
type(t1)

t2 = ('Single',)
type(t2)

t3 = 'x', 'y', 'z'
t3
type(t3)

M[1]
M[1] = 2.0

# Section 3.8
d1 = {'Stock A':30, 'Stock B':40}
d1['Stock A']

# Section 3.9
Winners = {'Company A','Company B'}
type(Winners)

Losers = set(['Company C', 'Company D'])
type(Losers)

Winners[0]

S0 = {}
S1 = set()
type(S0)
type(S1)

set('Quant')
type( set('Quant') )

{'Quant'}
type( {'Quant'} )

L1 = [1, 2, 3]
L2 = [2, 2, 1, 3, 3]
set(L1)
set(L2)

set(L1) == set(L2)