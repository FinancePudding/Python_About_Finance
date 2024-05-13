# -*- coding: utf-8 -*-
#1.
import datetime as dt

now = dt.datetime.now()

now.strftime('%Y-%m-%d')

#2.
def create_name():
    name = input('输入用户名\n')
    if ord(name[0])<65 or ord(name[0])>122:
        print('用户名必须以字母开头')
        return(create_name())
    else:
        return(name)

def verify_passwd(passwd):
    head = 65 <= ord(passwd[0]) <= 122
    contain_number = any([str(x) in passwd for x in range(9)])
    contain_symbol = any([str(x) in passwd for x in ('_','*','#')])
    return(head and (contain_number or contain_symbol))

def create_passwd():
    passwd = input('输入密码\n')
    is_legal = verify_passwd(passwd)
    if is_legal:
        return(passwd)
    else:
        return(create_passwd())
        
def create_account():
    create_name()
    create_passwd()
    print('用户创建成功')
    
create_account()   

#3.
 evens =[i+1 for i in range(100) if (i+1)%2==0]

#4.
#import datetime as dt
dates = [dt.datetime(2015,1,13)+dt.timedelta(i) for i in range(5)]
closes = [7.31,7.28,7.40,7.43,7.41]
prices = {dates[i]:closes[i] for i in range(5)}
prices[dt.datetime(2015,1,20)] = 7.44
dates.append(dt.datetime(2015,1,20))
prices[dt.datetime(2015,1,21)- dt.timedelta(4)]
prices[dt.datetime(2015,1,16)] = 7.50

#5.
import math
cash = 10000
share = {dates[0]:0}
for i in range(1,6):
    if prices[dates[i]]>prices[dates[i-1]]:
        buyshare = math.floor(0.5*cash/prices[dates[i]])
        share[dates[i]]= buyshare
        cash=cash-buyshare*prices[dates[i]]+share[dates[i-1]]*prices[dates[i]]
    else:
         share[dates[i]]= 0
share
