import os
import urllib
import warnings
import pymysql
import pandas as pd
from sqlalchemy import create_engine
warnings.filterwarnings('ignore')

"""
将常用的mysql数据库的地址和密码进行打包，方便直接通过Python连接获取数据，后续如果可以添加其他的数据库连接到数据库连接池中，方便直接调用。
"""

class QueryData:
    def connection_pool(self):
        '''
        如果公司中存在多个数据库，可以通过创建连接池的方法进行连接，只需要将数据库地址替换成自己的地址就可以。
        :param connect0: 数据库连接地址0
        :param connect1: 数据库连接地址1
        :param connect2: 数据库连接地址2
        :return db_pool: josn格式数据库连接池
        '''
        connect0 = {'host': 'localhost',
                    'port': 3306,
                    'user': 'root',
                    'passwd': '',
                    'db': ['stocks', 'etfs']}
        connect1 = {'host': '数据库1的地址',
                    'port': 3306,
                    'user': '用户名',
                    'passwd': '密码',
                    'db': ['子数据库1', '子数据库2']}
        connect2 = {'host': '数据库2的地址',
                    'port': 3306,
                    'user': '用户名',
                    'passwd': '密码',
                    'db': ['子数据库1', '子数据库2']}
        connect_pool = [connect0, connect1, connect2]
        return connect_pool

    def db_connect(self, connect_number: int, database_number: int):
        '''
        连接指定connect的数据库，并返回数据库和游标
        :param connect_number: 连接池的编号，从0开始
        :param database_number: 需要连接的db列表编号，从0开始
        :return conn, cursor: 返回数据库连接和游标
        '''
        db_pool = self.connection_pool()
        conn = pymysql.connect(host=db_pool[connect_number]['host'],
                               port=db_pool[connect_number]['port'],
                               user=db_pool[connect_number]['user'],
                               passwd=db_pool[connect_number]['passwd'],
                               db=db_pool[connect_number]['db'][database_number])
        cursor = conn.cursor()
        print(
            f"连接成功！您已连接connect{connect_number},正在使用{db_pool[connect_number]['db'][database_number]}数据库!")
        return conn, cursor

    def db_close(self, conn, cursor):
        '''
        关闭连接的数据库，可以降低缓存的占用，使运行速度更快
        :param conn: 数据库连接
        :param cursor: 数据库游标
        '''
        cursor.close()
        conn.close()
        print('数据库和游标已关闭！')

    def get_mysql_data(self, connect_number: int, database_number: int, sql: str) -> pd.DataFrame:
        '''
        连接指定数据库，并执行sql语句，返回结果
        :param connect_number: 连接池的编号，从0开始，代表需要连接的mysql主机端口
        :param database_number: 需要连接的db列表编号，从0开始，代表需要连接的mysql数据库
        :param sql: 需要执行的sql语句
        :return results: 返回查询结果，格式为DataFrame
        '''
        conn, cursor = self.db_connect(connect_number, database_number)
        result_df = pd.read_sql(sql, con=conn)
        self.db_close(conn, cursor)
        print(f"数据获取成功！数据预览如下：\n{result_df.head()}")
        return result_df

    def get_local_data_paths(self, file_path: str, data_suffix: str|list) -> list:
        '''
        获取本地文件数据
        :param file_path: 想要读取的文件路径
        :param data_suffix: 文件后缀名
        :return: 返回文件数据
        '''
        file_path_list = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if isinstance(data_suffix, str):
                    if file.endswith(data_suffix):
                        file_path_list.append(os.path.join(root, file))
                elif isinstance(data_suffix, list):
                    if file.endswith(tuple(data_suffix)):
                        file_path_list.append(os.path.join(root, file))
        return file_path_list

if __name__ == '__main__':
    qd = QueryData()
    sql = "select * from a_daily_post limit 10;"
    df = qd.get_mysql_data(connect_number=0, database_number=0, sql=sql)
