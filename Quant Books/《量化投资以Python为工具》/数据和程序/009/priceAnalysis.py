# -*- coding: utf-8 -*-

def OpenPrice(priceSequence):
    Open = priceSequence[0]
    return(Open)
    
def ClosePrice(priceSequence):  
    Close = priceSequence[-1]
    return(Close)
    
def HighPrice(priceSequence):
    High = priceSequence[0]
    for price in priceSequence:
        if price > High:
            High = price
    return(High)
    
def LowPrice(priceSequence):
    Low = priceSequence[0]
    for price in priceSequence:
        if price < Low:
            Low = price
    return(Low)