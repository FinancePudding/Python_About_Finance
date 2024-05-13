'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 4\\022')
'''

import pandas as pd
Index=pd.read_table('TRD_Index.txt',sep='\t',index_col='Trddt')
SHindex=Index[Index.Indexcd==1]
#查看前3期数据
SHindex.head(n=3)
#查看数据SHindex的类型
type(SHindex)
#提取上证综指的收盘指数数据
Clsindex=SHindex.Clsindex
Clsindex.head(n=3)
type(Clsindex)
type(Clsindex.index)
#将收盘指数转换成时间序列格式
Clsindex.index=pd.to_datetime(Clsindex.index)
Clsindex.head()
#查看Clsindex的类型
type(Clsindex)
#Clsindex的index是日期数据
type(Clsindex.index)
#最后，绘制时间序列图
Clsindex.plot()

#截取2014年10月8日到10月31日的数据
SHindex.index=pd.to_datetime(SHindex.index)
SHindexPart=SHindex['2014-10-08':'2014-10-31']
#查看前两期数据
SHindexPart.head(n=2)
#查看后两个交易数据
SHindexPart.tail(n=2)

#截取2015年数据
SHindex2015=SHindex['2015']
#查看2015年前2期交易数据
SHindex2015.head(n=2)
#查看后2期交易数据
SHindex2015.tail(n=2)

#选取2015年初以后的数据
SHindexAfter2015=SHindex['2015':]
SHindexAfter2015.head(n=2)
#选取2015年以前的数据
SHindexBefore2015=SHindex[:'2014-12-31']
SHindexBefore2015.tail(n=2)

#选取2014年9月到年底的数据
SHindex9End=SHindex['2014-09':'2014']
SHindex9End.head(n=2)
SHindex9End.tail(n=2)

Clsindex.head()
Clsindex.tail(n=1)
Clsindex.hist()
#求最大值
Clsindex.max()
#求最小值
Clsindex.min()
#求均值
Clsindex.mean()
#求中位数
Clsindex.median()
#求标准差
Clsindex.std()
#总结数据分布情况
Clsindex.describe()