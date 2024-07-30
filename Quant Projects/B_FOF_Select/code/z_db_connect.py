import pymysql


def db_cursor_connect(db_number: int, con_db_number: int):
    '''
    设置一个从数据库池中直接输入数据库编号号
    :param database_number:选取的数据库编号
    :param con_db_number:选取需要连接的子数据库编号
    :return:database,cursor:
    '''
    database0 = {'host': 'com',
                 'port': 3306,
                 'user': 'read',
                 'passwd': 'Alpha',
                 'db': ['dw-fund', 'dw-stock', ]}
    # 这个数据库主要使用QT_Papillon，进行文本新闻数据处理，使用Qwen大模型进行新闻文本数据处理的主要数据来源
    database1 = {'host': 'com.cn',
                 'port': 3306,
                 'user': 'ot_r1',
                 'passwd': 'n4',
                 'db': ['information_schema']}
    # 该数据库主要是用于获取日内或者分钟级别的数据,主要使用过dw-fusion-p中的bzsq_stock_tick_1m数据表获取分钟级别的数据，其他的数据库暂时没有使用过
    database2 = {'host': 'ncs.com',
                 'port': 3306,
                 'user': 'n_oper',
                 'passwd': 'G',
                 'db': ['ianlong']}
    # 设置成一个数据库池
    db_pool = [database0, database1, database2]
    # 连接数据库
    database = pymysql.connect(host=db_pool[db_number]['host'],
                               port=db_pool[db_number]['port'],
                               user=db_pool[db_number]['user'],
                               passwd=db_pool[db_number]['passwd'],
                               db=db_pool[db_number]['db'][con_db_number])
    # 设置游标
    cursor = database.cursor()
    print(f"连接成功！您已连接数据库{db_number},正在使用子数据库{db_pool[db_number]['db'][con_db_number]}!")
    return database, cursor


def db_cursor_close(databases, cursor):
    '''关闭连接的数据库'''
    cursor.close()
    databases.close()
    print('数据库和游标已关闭！')
