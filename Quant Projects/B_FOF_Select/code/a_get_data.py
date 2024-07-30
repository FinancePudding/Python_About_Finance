import pymysql
import pandas as pd
import numpy as np
import pickle
import exchange_calendars as xcals

'''
主要从本地的mysql数据库获取相应的数据，如果没有mysql数据库，可以自己下载安装一个MySQL社区版，自己在本地建立一个数据库，更加方便的进行数据管理操作。
数据获取的代码这里由于时间比较久远，而且数据丢失严重，大家可能会运行不同，所以这里会直接给大家最终获取的数据。最重要的是大家没有MySQL数据库，所以代码没办法运行。
我目前能找到部分数据，如果大家想要查看需要自己修改上面的路径。

这里需要安装交易所日历的包： pip install exchange_calendars, 具体的交易所代码可以参考相关官网文档。一般常用的是"XSHG"，即上海证券交易所。
'''

def connect_db():
    '''
    连接MySQL数据库
    '''
    databases = pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                passwd='password',
                                db='stocks')
    cursor = databases.cursor()
    return cursor, databases


def close_db(cursor, databases):
    '''
    关闭连接的数据库
    '''
    cursor.close()
    databases.close()
    print('数据库和游标已关闭！')


def exchange_date(start_date: str, end_date: str) -> tuple:
    """
    这里通过输入开始日期和结束日期，中国沪市的交易所交易日期
    :param start_date:'20210115'
    :param end_date:'20230115'
    :returns trade_date_tuple,返回元组格式的日期
    """
    xshg = xcals.get_calendar("XSHG")
    xshg_range = xshg.schedule.loc[start_date:end_date]
    trade_date_tuple = tuple(xshg_range.index.strftime("%Y%m%d"))
    return trade_date_tuple


def code_y_a():
    '''
    获取养老FOF基金Y份额的股票代码
    '''
    fund_data = pd.read_excel(r"D:\个人文件集\西筹科技实习\实习笔记\研究报告\养老主题\基准数据\FOF_Y.xlsx")
    fund_code = fund_data['基金代码'].astype(str).str.zfill(6)
    code_y_tuple = tuple(fund_code)
    # 获取主基金代码数据,这里的主基金数据只有163个，部分基金成立时间较晚，所以不在统计范围之列
    cursor, db = connect_db()
    cursor.execute(
        f'select distinct bsc_prim_code_mapping.main_code, fund_name,primary_code from bsc_prim_code_mapping where main_code in {code_y_tuple}')
    main_primary_code = pd.DataFrame(cursor.fetchall(), columns=['main_code', 'fund_name', 'primary_code'])
    main_primary_code.drop_duplicates(['main_code', 'primary_code'], inplace=True)
    main_primary_code.reset_index()
    code_a = main_primary_code['primary_code']
    code_a_tuple = tuple(code_a)
    close_db(cursor, db)
    return code_y_tuple, code_a_tuple


# 设置获取基金成立时间数据，净值数据，穿透权益数据函数
def setup_date(code_tuple):
    '''获取输入基金代码相应基金的成立时间'''
    cursor, db = connect_db()
    cursor.execute(f'select main_code,fund_name,setup_date from bsc_basics where main_code in {code_tuple}')
    Setup_date = pd.DataFrame(cursor.fetchall(), columns=['main_code', 'fund_name', 'setup_date'])
    close_db(cursor, db)
    return Setup_date


def nav_unit_data(code_tuple, start_date, end_date):
    '''获取基金的净值数据'''
    cursor, db = connect_db()
    trade_date_tuple = exchange_date(start_date, end_date)  # 这里是为了和基准日期保持一致，数据库中的净值数据存在非交易日依然有数据的情况
    cursor.execute(
        f"select fund_code, nav_date, nav_unit from fd_nav where fund_code in {code_tuple} and nav_date in {trade_date_tuple}")
    nav_unit_df = pd.DataFrame(cursor.fetchall(), columns=['fund_code', 'nav_date', 'nav_unit'])
    close_db(cursor, db)
    return nav_unit_df


def equity_data(code_tuple):
    '''获取基金的穿透权益数据'''
    cursor, db = connect_db()
    # 只获取中季度和年末的穿透权益数据，更加全面一点
    cursor.execute(f"select main_code,ann_date, end_date, stock_code, mktval_net_asset, report_type from annip_stk_invest_info_fof \
    where main_code in {code_tuple} and end_date in ('20191231','20200630', '20201231','20210630', '20211231','20220630','20221231','20230630','20231231')")
    equity = pd.DataFrame(cursor.fetchall(),
                          columns=['main_code', 'ann_date', 'end_date', 'stock_code', 'mktval_net_asset',
                                   'report_type'])
    # equity_drop_dup=equity.drop_duplicates(subset=['main_code', 'end_date', 'stock_code'])
    close_db(cursor, db)
    return equity


# 读取万得三只指数的收盘价数据，获取成分股的股票代码、穿透后的权益数据以及权益中枢的统计函数
def data_b_close_df(start_date, end_date):
    '''将三只基准指数数据的收盘价组成一个df数据框,同时获取指定日期内的数据'''
    data_b_l = pd.read_excel(r"D:\个人文件集\西筹科技实习\实习笔记\研究报告\养老主题\基准数据\885073.WI.xlsx")
    data_b_m = pd.read_excel(r"D:\个人文件集\西筹科技实习\实习笔记\研究报告\养老主题\基准数据\885074.WI.xlsx")
    data_b_s = pd.read_excel(r"D:\个人文件集\西筹科技实习\实习笔记\研究报告\养老主题\基准数据\885075.WI.xlsx")
    data_b_list = [data_b_l, data_b_m, data_b_s]
    data_b_close = []
    for df in data_b_list:
        df.set_index(pd.to_datetime(df["交易日期"]), inplace=True)
        # 对指数中的错误数据进行预处理
        df['收盘价'] = df['收盘价'].str.replace(',', '').astype(float)
        data_b_close.append(df['收盘价'])
    data_b_close = pd.DataFrame(np.array(data_b_close).T, index=pd.to_datetime(data_b_l["交易日期"]),
                                columns=['885073.WI', '885074.WI', '885075.WI'])
    data_b_close.sort_index(inplace=True)
    data_b_close = data_b_close[start_date:end_date]
    return data_b_close


def code_all_index_fof():
    '''
    从本地读取文件，分别获取万得指数中成分基金代码，权重为等额权重
    :return code_dict: 键值为股票代码，值为基金代码的元组的字典
    '''
    All_Index_FOF_Code = pd.read_excel(
        r"D:\个人文件集\西筹科技实习\实习笔记\研究报告\养老主题\万得基准指数成分及权重\Index_FOF_Code.xlsx")
    code_dict = {}
    for col in All_Index_FOF_Code.columns:
        code_float = All_Index_FOF_Code[col].dropna()
        code_int = code_float.astype(int)
        code_str = code_int.astype(str).str.zfill(6)
        code_dict[code_str.name] = tuple(code_str)
    return code_dict


def equity_all_index_fof(code_dict):
    '''
    获取三只万得指数成分基金，近4年的权益中枢数据
    :param code_dict: 包含三只指数成分基金的代码数据
    :return equity_dict: 包含所有成分基金的权益数据
    '''
    equity_dict = {}
    for i in code_dict.keys():
        index_equity = equity_data(code_dict[i])
        equity_dict[i] = index_equity
    return equity_dict


def equity_center_data(equity_index):
    '''
    获取三只指数的权益中枢数据
    :param equity_index:指数的指定时间范围内的成分权益数据
    :return equity_center_dict:权益中枢字典
    '''
    equity_center_dict = {}
    for i in equity_index.keys():
        # 对权益进行分类统计
        equity_index_gourp1 = pd.DataFrame(equity_index[i].groupby(['end_date', 'main_code'])['mktval_net_asset'].sum())
        # 计算各个报告期的权益中枢均值
        equity_index_gourp2 = pd.DataFrame(equity_index_gourp1.groupby(['end_date'])['mktval_net_asset'].mean())
        equity_center_dict[i] = equity_index_gourp2
    return equity_center_dict


def main():
    # 设置时间
    start_date = '20200101'
    start_date_1year = '20230101'
    end_date = '20240101'
    # 获取基金代码
    code_y_tuple, code_a_tuple = code_y_a()
    # 获取A基金近四年的成立时间，净值数据，权益数据
    a_setup_date = setup_date(code_a_tuple)
    a_nav_unit_data = nav_unit_data(code_a_tuple, start_date, end_date)
    a_equity_data = equity_data(code_a_tuple)
    # 获取Y基金近一年的净值数据,成立时间
    y_nav_unit_data = nav_unit_data(code_y_tuple, start_date_1year, end_date)
    y_setup_date = setup_date(code_y_tuple)
    # 获取业绩比较基准收盘价数据
    b_close_df = data_b_close_df(start_date, end_date)
    b_comp_code_dict = code_all_index_fof()
    b_comp_equity = equity_all_index_fof(b_comp_code_dict)
    b_comp_equity_center = equity_center_data(b_comp_equity)
    # 将全部数据存储在字典中
    data_dict = {
        'a_setup_date': a_setup_date,
        'a_nav_unit_data': a_nav_unit_data,
        'a_equity_data': a_equity_data,
        'y_nav_unit_data': y_nav_unit_data,
        'y_setup_date': y_setup_date,
        'b_close_df': b_close_df,
        'b_comp_code_dict': b_comp_code_dict,
        'b_comp_equity': b_comp_equity,
        'b_comp_equity_center': b_comp_equity_center
    }
    return data_dict


if __name__ == '__main__':
    data_dict = main()
    # 保存文件为pickle格式
    file_path = r'D:\个人文件集\西筹科技实习\Qwen-finetune-new\qwen-finetune\qwen-finetune\FOF_NEW\data_dict.pkl'
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data_dict, f)
        print("Data successfully saved.")
    except Exception as e:
        print(f"Error:{e}")