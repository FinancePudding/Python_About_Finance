# -*- coding: utf-8 -*-
#1、
class account:
    def __init__(self,name,balance):
        self.name=name
        self.balance=balance
    
    def deposit(self,amount):
        self.balance += amount
    
    def withdraw(self,amount):
        if amount>self.balance:
            print('余额不足，交易失败')
        else:
            self.balance -= amount

sam = account('Sam',1000)
sam.deposit(500)
sam.withdraw(1200)
sam.balance

class account:
    def __init__(self,name,balance):
        self.name=name
        self.__balance=balance
    
    def deposit(self,amount):
        self.__balance += amount
    
    def withdraw(self,amount):
        if amount>self.balance:
            print('余额不足，交易失败')
        else:
            self.__balance -= amount
    
    def get_balance(self):
        return(self.__balance)
        
    def set_balance(self,amount):
        self.__balance = amount

#2、
class account:
    def __init__(self,name,balance):
        self.name=name
        self.__balance=balance
    
    def deposit(self,amount):
        self.__balance += amount
    
    def withdraw(self,amount):
        if amount>self.__balance:
            print('余额不足，交易失败')
        else:
            self.__balance -= amount
    
    def get_balance(self):
        return(self.__balance)
        
    def set_balance(self,amount):
        self.__balance = amount
        
    def transfer(self,amount,target):
        if amount>self.__balance:
            print('余额不足，交易失败')
        else:
            target.deposit(amount)
            self.withdraw(amount)
            
sam = account('Sam',1000)
john = account('John',3000)
john.transfer(1000,sam)

#3、
class check(account):
    
    def __init__(self,name,balance,credit):
        self.name = name
        self.__balance = balance
        self.credit = credit
        self.overdraft = 0
        
    def deposit(self,amount):
        if self.overdraft > 0 and self.overdraft-amount < 0:
            self.__balance = amount - self.overdraft
            self.overdraft = 0
        elif self.overdraft > 0:
            self.overdraft -= amount
        else:
            self.__balance += amount
    
    def withdraw(self,amount):
        if self.__balance==0 and amount + self.overdraft > self.credit:
            print('超出信用額度，交易失败')
            return(1)
        elif self.__balance==0:
            self.__overdraft += amount
            return(0)
        elif 0 < self.__balance < amount and amount - self.__balance <=self.credit:
            self.overdraft = amount - self.__balance
            self.__balance=0
            return(0)
        elif 0 < self.__balance < amount:
            print('超出信用額度，交易失败')
            return(1)
        else:
            self.__balance -= amount
            return(0)
        
    def transfer(self,amount,target):
        result = self.withdraw(amount)
        if result == 0:
            target.deposit(amount)
        
            
sam = check('Sam',1000,1000)
sam.withdraw(700)
sam.withdraw(1500)