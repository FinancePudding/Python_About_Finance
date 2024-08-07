import warnings
import rqdatac as rq
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
warnings.filterwarnings('ignore')

rq.init(username='license', password=open(r'D:\My_Github\Passwards\rice_quant_edu.txt').read())


'''
对常用的数据预处理方法进行封装操作，目前包括：中性化处理、异常值处理等。

异常值处理，设置缩尾法，三倍标准差法，绝对值中位差法等不同的方法对因子数据进行异常值处理，主要是去除其中的极值
缩尾法和绝对值中位差法是最常用的做法，绝对值中位差的方法去除的极值更多一些，可以通过设置不同的阈值进行拓宽。
'''


def neutralization(stock_data: pd.DataFrame, factor_name: str, market_name: str, ind_name: str = None) -> pd.DataFrame:
    '''
    中性化处理，一般包括是市值中性化、市值行业中性化等。
    :param stock_data: 股票数据截面，包含因子值、市值、行业数据等。
    :param factor_name: 因子名称的列名
    :param market_name: 市值名称的列名
    :param ind_name: 行业名称所在列的列名
    :return:
    '''
    x_cols = [market_name]
    # 判断是否需要进行行业中性化处理
    if ind_name is not None:
        stock_data = pd.concat([stock_data, pd.get_dummies(stock_data[ind_name], prefix='申万一级行业_', drop_first=True, dtype=float)], axis=1)
        x_cols += [ind_dummy for ind_dummy in stock_data.columns if ind_dummy.startswith('申万一级行业_')]
    else:
        pass
    X = stock_data[x_cols]
    Y = stock_data[[factor_name]]
    model = LinearRegression()
    model.fit(X, Y)
    stock_data[f'{factor_name}_neutralized'] = Y.values - model.predict(X)
    return stock_data


def winsorization(stock_data: pd.DataFrame, factor_name: str, p: float = 0.01, method: str='keep') -> pd.DataFrame:
    '''
    缩尾法又被称为固定比例法，即按照变量从小到大进行排序，将小于p分位数和大于1-p分位数的指标值剔除（或者用临界点值替代）。
    :param stock_data: 默认是截面的股票数据，包含需要缩尾的因子值 ['交易日期', '股票代码', '因子名称']
    :param factor_name: 需要缩尾的因子名称
    :param p: 判断异常值的分位数，默认0.01，即对小于p分位数和大于1-p分位数的指标值确定为异常值
    :param method: 处理方式，keep表示保留异常值，用临界点值替代，drop表示直接删除异常值
    :return df: 缩尾处理后的因子数据
    '''
    stock_data = stock_data.dropna(subset=[factor_name])
    stock_data = stock_data.sort_values(by=[factor_name])
    # 计算因子数据进行排序，排除异常值处理
    stock_data[f'{factor_name}_排名'] = stock_data[factor_name].rank() / len(stock_data)
    if method == 'keep':
        df = stock_data.copy()
        df[factor_name] = df.apply(
            lambda row: np.nan if row[f'{factor_name}_排名'] < p or row[f'{factor_name}_排名'] > 1-p else row[factor_name],
            axis=1
        )
        df = df.bfill().ffill()
    elif method == 'drop':
        df = stock_data.query(f'{factor_name}_排名 >= {p} and {factor_name}_排名 <= {1-p}')
    else:
        print('请输入正确的method参数，keep或drop')
    return df

def sigma3_std(stock_data: pd.DataFrame, factor_name: str, sigma_multiple: float = 3, method: str='keep') -> pd.DataFrame:
    '''
    标准差法去除极值，指定范围标准差之外的数据确认为异常值数据，对其进行删除或者使用临界值进行填充的方法。
    :param stock_data: 默认是截面的股票数据，包含需要缩尾的因子值 ['交易日期', '股票代码', '因子名称']
    :param factor_name: 需要缩尾的因子名称
    :param sigma_multiple: 标准差乘数，指定范围标准差之外的数据确认为异常值数据, 默认3, 即3倍标准差之外的数据为异常值数据
    :param method: 处理方式，keep表示保留异常值，用临界点值替代，drop表示直接删除异常值
    :return df: 标准差处理后的因子数据
    '''
    stock_data = stock_data.dropna(subset=[factor_name])  # 去除缺失值
    stock_data = stock_data.sort_values(by=[factor_name]) # 排序
    mean = stock_data[factor_name].mean()
    std = stock_data[factor_name].std()
    if method == 'keep':
        df = stock_data.copy()
        df[factor_name] = df.apply(
            lambda row: np.nan if abs(row[factor_name] - mean) > sigma_multiple * std else row[factor_name],
            axis=1
        )            # 将异常值替换为nan，方便进行后续的向前填充和向后填充。
        df = df.bfill().ffill()   # 将临界值向前向后填充
    elif method == 'drop':
        df = stock_data.query(f'({mean - sigma_multiple * std}) <= {factor_name} <= ({mean + sigma_multiple * std})')
    else:
        print('请输入正确的method参数，keep或drop。')
    return df

def median_absolute_deviation(stock_data: pd.DataFrame, factor_name: str, MAD_e_multiple: float = 3, method: str='keep'):
    '''
    绝对值中位差法，考虑到样本均值和标准差不够稳健，容易受到异常值的影响，因此将均值用中位数代替，将标准差用绝对中位差代替，这样就得到了MAD法。
    :param stock_data: 默认是截面的股票数据，包含需要缩尾的因子值 ['交易日期', '股票代码', '因子名称']
    :param factor_name: 需要处理异常值的因子名称
    :param MAD_e_multiple: 偏离程度乘数，指定范围偏离程度之外的数据确认为异常值数据, 默认3, 即3倍偏离程度之外的数据为异常值数据
    :param method: 处理方式，keep表示保留异常值，用临界点值替代，drop表示直接删除异常值
    :return df: 绝对值中位差处理后的因子数据
    '''
    stock_df = stock_data.dropna(subset=[factor_name])
    stock_df = stock_df.sort_values(by=[factor_name])  # 排序
    Xm = np.median(stock_df[factor_name])
    MAD = np.median(abs(stock_df[factor_name] - Xm))
    MAD_e = MAD * 1.4826  # 1.4826是MAD的变换系数, 得到最终的偏离程度
    if method == 'keep':
        df = stock_df.copy()
        df[factor_name] = df.apply(
            lambda row: np.nan if abs(row[factor_name] - Xm) > MAD_e_multiple * MAD_e else row[factor_name],
            axis=1
        )
        df = df.bfill().ffill()
    elif method == 'drop':
        df = stock_df.query(f'({Xm - MAD_e_multiple * MAD_e}) <= {factor_name} <= ({Xm + MAD_e_multiple * MAD_e})')
    else:
        print('请输入正确的method参数，keep或drop。')
    return df

if __name__ == '__main__':
    # 获取沪深300成分股数据
    hs300_components = rq.index_components('000300.XSHG')
    hs300_components_df = rq.get_price(hs300_components, start_date='2023-08-01', end_date='2024-08-01')
    hs300_components_df.reset_index(inplace=True)
    hs300_components_df.to_csv(r'D:\My_Github\Python_About_Finance\Quant Tool\test_data\hs300_components_df.csv')
    # 获取申万一级行业成分股数据：https://www.swsresearch.com/institute_sw/allIndex/releasedIndex
    sw_ind_info = pd.read_excel(r'D:\My_Github\Python_About_Finance\Quant Tool\test_data\申万一级行业划分.xlsx')
    sw_ind_info['指数代码'] = sw_ind_info['指数代码'].astype(str)
    rq_sw_codes = [f'{code}.INDX' for code in sw_ind_info['指数代码'].tolist()]
    # 获取申万一级行业成分股数据
    sw_comp_codes = {}
    for rq_sw_code in rq_sw_codes:
        sw_comp_codes[rq_sw_code] = rq.index_components(rq_sw_code)
    # 将其转化为dataframe格式
    ind_comp = []
    for key in rq_sw_codes:
        ind_comp += [[key, i] for i in sw_comp_codes[key]]
    sw_ind_comp_df = pd.DataFrame(ind_comp, columns=['行业代码', '成分股代码'])
    sw_ind_comp_df['指数代码'] = sw_ind_comp_df['行业代码'].str[0:6]

    sw_ind_comp_df = pd.merge(sw_ind_comp_df, sw_ind_info[['指数代码', '指数名称']], how='left', on='指数代码')
    sw_ind_comp_df.to_csv(('./Python_About_Finance/Quant Tool/test_data/申万一级行业成分股对照表.csv'))
    # 将沪深300指数与申万一级行业指数进行对应
    hs300_stock_ind = pd.merge(hs300_components_df, sw_ind_comp_df, how='left', left_on='order_book_id', right_on='成分股代码')
    hs300_stock_ind.rename(columns={'指数名称': '行业名称'}, inplace=True)
    hs300_stock_ind.drop(columns=['指数代码'], inplace=True)
    hs300_stock_ind.drop(columns=['成分股代码'], inplace=True)
    hs300_stock_ind.to_csv(r'D:\My_Github\Python_About_Finance\Quant Tool\test_data\hs300_stock_ind.csv')

    stock_data = hs300_stock_ind.copy()

