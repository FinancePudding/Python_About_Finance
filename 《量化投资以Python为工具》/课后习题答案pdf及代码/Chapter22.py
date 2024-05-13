import pandas as pd
import matplotlib.pyplot as plt

#2.
Yen=pd.read_csv('Data/Part4/001/Yen.csv',index_col='date')
Yen.index=pd.to_datetime(Yen.index,format='%Y%m%d')

#3.
Yen.s.plot()

#4.
pfyh=pd.read_csv('Data/Part4/001/pfyh.csv',index_col='Date')
pfyh.index=pd.to_datetime(pfyh.index,format='%Y-%m-%d')
returns=(pfyh.Close-pfyh.Close.shift(1))/pfyh.Close.shift(1)
returns=returns[1:]
returns.plot() 