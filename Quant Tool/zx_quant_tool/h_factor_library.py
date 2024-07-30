import pandas as pd
import numpy as np
import tushare as ts

'''
编制相关因子计算公式

卡玛比率
区间收益率
最大回撤
日度波动率
年化波动率
信息比率
夏普比率
特雷诺比率
'''
cal_col = 'close'

class FactorLibrary:
    '''
    FactorLibrary 类，用于计算股票相关的各类因子数据。
    '''
    def __init__(self):
        pass

    def daily_return(self, df: pd.DataFrame, cal_col:str = 'close', method: str = 'simple') -> pd.DataFrame:
        '''
        计算日收益率，可以选择对数收益率和简单收益率两种方法进行相应的计算处理，默认使用简单收益率。
        :param df: 股票的时间序列数据，包含 ['ts_code', 'open', 'high', 'low', 'close', 'vol', 'amount'] 列
        :return cal_col: 收盘价列名，默认值为 'close'
        :return method: 计算方法，默认值为'simple'，可选值为 【'simple', 'log'】，分别表示简单收益率和对数收益率
        :return df: 计算后的时间序列数据，包含 ['daily_return'] 列
        '''
        if method =='simple':
            df['daily_ret_simple'] = df[cal_col].pct_change()
        elif method == 'log':
            df['daily_ret_log'] = np.log(df[cal_col] / df[cal_col].shift(1))
        return df

    def annual_return(self, df: pd.DataFrame, cal_col:str = 'close', method: str = 'simple') -> pd.DataFrame:
        '''
        计算年化收益率
        :param df: 股票的时间序列数据，包含 ['ts_code', 'open', 'high', 'low', 'close', 'vol', 'amount'] 列
        :return cal_col: 收盘价列名，默认值为 'close'
        :return df: 计算后的时间序列数据，包含 ['annual_return'] 列
        '''
        if method =='simple':
            df_ret = self.daily_return(df, cal_col, method)
            df_ret.fillna(0)
        df['daily_ret_simple'] = df[cal_col].pct_change()
        df['annual_return'] = (1 + df['daily_ret_simple']).cumprod() ** 252 - 1
        return df

def sharpe_ratio(df: pd.DataFrame, cal_col:str = 'close', rf: float=0.0):
    '''
    计算夏普比率：Sharpe Ratio = (E(R) - Rf) / std(R)
    :param df:
    :return:
    '''

if __name__ == '__main__':
    pro = ts.pro_api(open(r'D:\My_Github\Passwards\tushare.txt', 'rb').read())
    # 获取不同股票的时间序列数据
    stock1 = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20190718')
    stock2 = pro.daily(ts_code='000004.SZ', start_date='20180701', end_date='20190718')
    stock2['trade_date'] = pd.to_datetime(stock2['trade_date'])
    stock2.set_index('trade_date', inplace=True)
    # 合并成面板数据
    df = pd.concat([stock1, stock2])
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    # 后续的所有因子计算都是基于股票的时间序列数据计算得到的，面版数据可以使用groupby函数进行分组操作传入