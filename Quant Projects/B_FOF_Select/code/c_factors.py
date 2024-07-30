import os

import numpy as np
import pandas as pd

os.chdir(r'E:\西筹科技实习\projects\i_fof_select')  # 设置工作目录

'''
设置计算因子的函数，大致可以分为：收益率因子、风险因子、风险收益比因子
'''
def anlzd_ret(nav_unit):
    '''
    计算基金的年化收益率
    :param nav_unit: 基金的日度净值数据, 索引是时间，列名是基金名称，值是基金的净值数据
    :return anlzd_r: 年化收益率
    '''
    ret = np.log(nav_unit / nav_unit.shift(1)).dropna()
    anlzd_r = ret.mean() * 252
    return anlzd_r


def anlzd_excess_ret(nav_unit, benchmark):
    '''
    计算基金的年化超额收益率
    :param nav_unit: 基金的日度净值数据
    :param benchmark: 基准指数的收盘价数据
    :return: 年化超额收益率
    '''
    anlzd_r = anlzd_ret(nav_unit)
    anlzd_r_b = anlzd_ret(benchmark)
    return anlzd_r - anlzd_r_b


def anlzd_std(nav_unit):
    '''
    计算基金的年化波动率
    :param nav_unit: 基金净值
    :return anlzd_ret_std: 年化波动率
    '''
    ret = np.log(nav_unit / nav_unit.shift(1)).dropna()
    anlzd_ret_std = ret.std() * np.sqrt(252)
    return anlzd_ret_std


def sharpe_ratio(nav_unit):
    '''
    计算基金的夏普比率
    :param nav_unit: 基金的日度净值数据
    :return sharpe_rat: 夏普比率
    '''
    r = anlzd_ret(nav_unit)
    rf = 0
    sigma = anlzd_std(nav_unit)
    sharpe_rat = (r - rf) / sigma
    return sharpe_rat


def max_drawdown(nav_unit):
    '''
    计算基金的最大回撤数据，这种算法相比于书中写的双循环的嵌套结构更加快速。既可以计算单个基金的数据，也可以计算多个基金的df组合数据。
    :param nav_unit: 基金的日度净值数据
    :return max_drawdown: 最大回撤数据
    '''

    def MDD(nav_unit):
        N_r = nav_unit.shape[0]
        DD = np.zeros((N_r - 1, N_r - 1))
        # 使用向量化操作计算 DD
        for i in range(N_r - 1):
            Pi = nav_unit[i]
            Pj = nav_unit[i + 1:]
            DD[i, :N_r - i - 1] = (Pi - Pj) / Pi
        Max_DD = np.max(DD)
        return Max_DD

    N_c = nav_unit.shape[1]
    if N_c == 0:
        return MDD(nav_unit)
    else:
        return nav_unit.apply(MDD, axis=0)


def calmar_ratio(nav_unit):
    '''
    计算单只基金的卡玛比率
    :param nav_unit: 基金的日度净值数据
    :return: 卡玛比率
    '''
    r = anlzd_std(nav_unit)
    rf = 0
    MDD = max_drawdown(nav_unit)
    return (r - rf) / MDD


def info_ratio(data, benchmark):
    '''
    计算信息比率（Information ratio）
    :param data: 基金的日度净值数据
    :param benchmark: 基准指数的收盘价数据
    :return: 信息比率
    '''
    Rp_daily = np.log(data / data.shift(1)).dropna()
    Rp = 252 * Rp_daily.mean()
    index = Rp.index
    Rp_array = np.array(252 * Rp_daily.mean())
    Rb_daily = np.log(benchmark / benchmark.shift(1)).dropna()
    Rb_daily = Rb_daily[Rp_daily.index]
    Rb_array = np.array(252 * Rb_daily.mean())
    TD = np.zeros_like(Rp_daily)
    for i in range(len(Rp)):
        TD[:, i] = np.array(Rp_daily.iloc[:, i]) - np.array(Rb_daily.iloc[0])
    TE = TD.std(axis=0) * np.sqrt(252)
    info_r = (Rp_array - Rb_array) / TE
    info_df = pd.Series(info_r, index=index)
    return info_df


def semi_stdev(nav_unit):
    '''
    计算基金的下行风险
    :param nav_unit: df,series形式，表示基金的净值数据，可以是一只基金，也可以是多只基金组合。
    :return semi_stdev: 下行风险
    '''
    r = np.log(nav_unit / nav_unit.shift(1))
    rf = 0
    return_neg = np.minimum(r - rf, 0)
    N_down = np.zeros_like(anlzd_std(nav_unit))
    for i in range(len(N_down)):
        N_down[i] = len(return_neg.iloc[:, i][return_neg.iloc[:, i] < 0])
    semi_stdev = np.sqrt(252 * np.sum(return_neg ** 2) / len(N_down))
    return semi_stdev


def sortino_ratio(nav_unit):
    '''
    计算索提诺比率
    :param nav_unit: 基金的日度净值数据
    :return: 索提诺比率
    '''
    r = anlzd_ret(nav_unit)
    rf = 0
    sigma_d = semi_stdev(nav_unit)
    return (r - rf) / sigma_d


def treynor_ratio(nav_unit, benchmark):
    '''
    计算特雷诺比率
    :param nav_unit: 基金的日度净值数据
    :param data_b_close: 基准指数的收盘价数据
    :return: 特雷诺比率
    '''
    import statsmodels.api as sm
    Rp_daily = np.log(nav_unit / nav_unit.shift(1)).dropna()
    Rp = 252 * Rp_daily.mean()
    Rf = 0
    data_b_close = data_b_close[Rp_daily.index]
    index_addcons = sm.add_constant(data_b_close)
    betas = np.zeros_like(Rp)
    for i in range(len(Rp)):
        model = sm.OLS(endog=Rp_daily, exog=index_addcons)
        result = model.fit()
        betas[i] = result.params[1]
    funds_TR = (Rp - Rf) / betas


if __name__ == '__main__':
    benchmark = pd.read_pickle(r'E:\西筹科技实习\projects\i_fof_select\FOF\FOF_new\data_fof\Data_B_Close.pkl')
    nav_unit = pd.read_pickle(r'E:\西筹科技实习\projects\i_fof_select\FOF\FOF_new\data_fof\Data_A_U_L.pkl')
