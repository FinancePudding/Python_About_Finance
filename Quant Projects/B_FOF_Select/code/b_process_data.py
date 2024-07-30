
import re
import os
import numpy as np
import pandas as pd

'''
对获取的原始数据进行相应的预处理操作，并进行相应的存储。这里数据预处理的方法不是太好，但是大家可以都尝试一下，具体可以自己运行debug一下。

这里数据预处理的方法比较蠢，这个项目是我刚开始做的，所以大家多多包涵。后面有时间重新写一遍。
'''

def FOF_Connect(FOF_Y):
    '''
    对原始净值数据进行横向拼接处理，并按照时间序列进行排序并计算对数收益率
    :param FOF_Y: 原始净值数据
    :return: 处理后的净值数据
    '''
    Grouped_Y_Dfs = []
    for name, group in FOF_Y.groupby('fund_code'):
        group['nav_date'] = pd.to_datetime(group['nav_date'])
        group.set_index('nav_date', inplace=True)
        group.sort_index(inplace=True)
        group['nav_unit'] = group['nav_unit'].astype('float64')
        group['p_change'] = (np.log(group['nav_unit'] / group['nav_unit'].shift(1))).dropna()
        group = group.rename(columns={'p_change': 'p_change' + f'_{name}', 'nav_unit': 'nav_unit' + f'_{name}'})
        Grouped_Y_Dfs.append(group)
    FOF_Y_df = pd.concat(Grouped_Y_Dfs, axis=1)
    return FOF_Y_df


def Y_describe():
    '''
    对成立满一年的Y份额基金2023年以来的对数收益率进行描述进行描述性统计
    '''
    y_nav_unit_data = data_dict['y_nav_unit_data']
    y_setup_date = data_dict['y_setup_date']
    y_1year_code_tuple = tuple(y_setup_date.query("setup_date<'20230101'")['main_code'])
    y_nav_unit_data_1year = y_nav_unit_data.query(f'fund_code in {y_1year_code_tuple}')
    y_connect_1year_df = FOF_Connect(y_nav_unit_data_1year)
    Data_Y_sum = y_connect_1year_df.filter(like='p_change', axis=1).sum()
    Data_Y_sum.describe()
    return Data_Y_sum


def A_Count(FOF_A_Set_date):
    '''
    对A基金各个年份成立数量进行统计
    :param FOF_A_Set_date: A基金的成立日期数据
    :return: 各个年份成立数量
    '''
    date = FOF_A_Set_date['setup_date']
    date = pd.to_datetime(date, format='%Y%m%d')
    date = date.dt.year.astype(str)
    FOF_A_Set_date['Year'] = date
    FOF_Count = FOF_A_Set_date['Year'].value_counts().sort_index()
    return FOF_Count


def Equity_Degree(df):
    '''
    根据穿透的权益数据对FOF基金进行分类, 按照权益中枢数据进行划分，分成低中高风险
    :param df: 穿透的权益数据
    :return: 低中高风险的A基金数据
    '''
    grouped_df = df.groupby(['main_code', 'end_date']).agg({'mktval_net_asset': 'sum'}).reset_index()
    result_df = grouped_df.groupby('main_code')['mktval_net_asset'].mean().reset_index()
    FOF_A_E = result_df.sort_values('mktval_net_asset').reset_index(drop=True)
    FOF_A_E_Small = FOF_A_E.query('mktval_net_asset <= 30').reset_index(drop=True)
    FOF_A_E_Mid = FOF_A_E.query('30 < mktval_net_asset < 55').reset_index(drop=True)
    FOF_A_E_Large = FOF_A_E.query('mktval_net_asset >= 55').reset_index(drop=True)
    return FOF_A_E_Small, FOF_A_E_Mid, FOF_A_E_Large


def Nav_Unit_degree(a_nav_unit_data, a_equity_data):
    '''
    按照权益中枢划分的低中高代码，分别获取三类划分标准的净值数据
    :param a_nav_unit_data: A基金的净值数据
    :param a_equity_data: A基金的权益数据
    :return: 低中高风险的A基金的净值数据
    '''
    FOF_A_3years = FOF_Connect(a_nav_unit_data)
    FOF_A_3years_nav_unit = FOF_A_3years.filter(like='nav_unit', axis=1)
    FOF_A_3years_nav_unit = FOF_A_3years_nav_unit.interpolate(method='linear', limit_area='inside')
    FOF_A_3years_nav_unit.dropna(inplace=True)
    Data_A_E_S, Data_A_E_M, Data_A_E_L = Equity_Degree(a_equity_data)
    code_s = list('nav_unit_' + Data_A_E_S['main_code'])
    Data_A_U_S = FOF_A_3years_nav_unit[code_s]
    code_m = list('nav_unit_' + Data_A_E_M['main_code'])
    Data_A_U_M = FOF_A_3years_nav_unit[code_m]
    code_l = list('nav_unit_' + Data_A_E_L['main_code'])
    Data_A_U_L = FOF_A_3years_nav_unit[code_l]
    return Data_A_U_S, Data_A_U_M, Data_A_U_L

#%%
if __name__ == '__main__':
    data_dict = pd.read_pickle('D:\My_Github\Projects_data\B_FOF_Select\data\output\data_dict.pkl')
    # 将字典中存储的数据全部添加到全局变量之中
    for key, value in data_dict.items():
        globals()[key] = value
    # 对函数进行相应的调试处理
    data = FOF_Connect(y_nav_unit_data)
    Data_Y_sum = Y_describe()
    a_nav_unit = FOF_Connect(a_nav_unit_data)



