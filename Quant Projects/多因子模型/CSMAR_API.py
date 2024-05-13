from csmarapi.CsmarService import CsmarService
import pandas as pd    
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
csmar = CsmarService()

# 用户名是相应学校的教育邮箱
username='xxxx@edu.com.cn'
# 登陆密码
password='abcd123'
# 登录
csmar.login(username, password,'0')
 
# 定义一个可以将CSMAR数据库中的数据格式转换成DataFrame格式的文档
def to_df(dic):
    cols = list(dic[0].keys())
    row_num = len(dic)
    lists=[[dic[0][key]]*row_num for key in cols]
    for i in range(1,row_num):
        for j,key in enumerate(cols):
            lists[j][i]=dic[i][key]
    df=pd.DataFrame({col:value for col,value in zip(cols,lists)})
    return df

#  获取个人账户中所购买的数据库列表，并全部打印出来。
def Database():
    database = csmar.getListDbs()
    database = to_df(database)
    return database

# 获取具体数据库中的数据表以及相应的数据字典
def Tables(Database_Name):
    Tables = csmar.getListTables(Database_Name)
    Tables = to_df(Tables)
    return Tables

# 进行数据预览以及具体字段的查询
def Fields_And_Preview(Tables_Name):
    Fields = csmar.getListFields(Tables_Name)
    Fields=to_df(Fields)
    Preview = csmar.preview(Tables_Name)
    Preview=to_df(Preview)
    return Fields,Preview

# 请求获取数据
def query(columns_list,condition_factor,tableName_factor,start_date,end_date):
    df=csmar.query_df(columns_list,condition_factor,tableName_factor,start_date,end_date)
    return df

def get_data():
    Database1=Database()
    Database1_Name=Database1.databaseName
    print('1.尊敬的VIP用户，您购买的数据如下：\n',Database1_Name)
    z=int(input('请输入您想要查询的数据库索引：\n'))
    #获取数据库中的所有的数据表清单
    Tables1=Tables(Database1_Name[z])
    Tables1_Name=Tables1.iloc[:,0:2]
    print('2.在%s数据库中所包含所有表格如下：\n'%Database1_Name[z],Tables1_Name)
    #获取数据预览和表格所含数据类型
    m=int(input('请输入您想要获取的数据表格索引：\n'))
    Fields1,Data1=Fields_And_Preview(Tables1.iloc[:,0][m])
    print('3.%s数据表中包含的内容如下：\n'%Tables1.iloc[:,0][m],Fields1)
    print('4.%s数据表的预览如下：\n'%Tables1.iloc[:,0][m],Data1.head(10))
    tableName=Tables1.iloc[:,0][m]
    #这里默认输出所有列的数据
    columns=list(Data1.columns)
    condition=str(input('请输入您筛选数据的条件：\n'))
    start_date=input("请输入您想要获取数据的开始日期，例如'2010-01-01':\n")
    end_date=input("请输入您想要获取数据的结束日期，例如'2010-02-01':\n")
    df=query(columns, condition, tableName, start_date, end_date)
    print('5.您选择导出数据预览如下：\n',df.head())
    print('数据导出成功！')
    return df

