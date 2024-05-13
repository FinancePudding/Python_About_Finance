# -*- coding: utf-8 -*-
import pmath

def OpenPrice(priceSequence):
    Open = priceSequence[0]
    return(Open)
    
def ClosePrice(priceSequence):  
    Close = priceSequence[-1]
    return(Close)
    
def HighPrice(priceSequence):
    High = pmath.findMax(priceSequence)    
    return(High)
    
def LowPrice(priceSequence):
    Low = pmath.findMin(priceSequence)
    return(Low)