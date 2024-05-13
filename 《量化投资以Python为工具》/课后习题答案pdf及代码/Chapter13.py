# -*- coding: utf-8 -*-

import pandas as pd
#1.
history = pd.read_csv('Data/Part2/001/history.csv',
                      index_col = 'Date')

history.index = pd.to_datetime(history.index,format='%Y-%m-%d')
history.head()
history['Emerging.Markets'].mean()
history['Emerging.Markets'].median()
history['Emerging.Markets'].mode()
history['Emerging.Markets'].quantile([0.1,0.9])

#2.
history['Event.Driven'].max() - history['Event.Driven'].min()
history['Event.Driven'].mad()
history['Event.Driven'].var()
history['Event.Driven'].std()

#3.
history[['Relative.Value','Fixed.Income.Arbitrage']].plot()
history['Relative.Value'].mean() 
history['Fixed.Income.Arbitrage'].mean() 
history['Relative.Value'].std() 
history['Fixed.Income.Arbitrage'].std() 

#4.
history.describe()
