import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

mysql_host = 'localhost'
mysql_db = 'weibo_data'
mysql_user = 'root'
mysql_pwd = '123456'
mysql_table = 'weibo_data_summary'

engine = create_engine('mysql+mysqlconnector://{}:{}@{}:3306/{}?charset=utf8mb4'.format(mysql_user, mysql_pwd, mysql_host, mysql_db))

data = pd.read_csv('..\data\sum\sum_emoscore.csv')

data['微博作者'] = data['微博作者'].astype('string') 
data['发布时间'] = data['发布时间'].astype('string') 
data['微博内容'] = data['微博内容'].astype('string') 
data['发布于'] = data['发布于'].astype('string') 
data['ip属地_城市'] = data['ip属地_城市'].astype('string') 
data['ip属地_省份'] = data['ip属地_省份'].astype('string') 
data['ip属地_国家'] = data['ip属地_国家'].astype('string') 
data['url链接'] = data['url链接'].astype('string') 
data['目标国家'] = data['目标国家'].astype('string') 

conn = pymysql.connect(host='localhost',user='root',passwd='123456',db = 'weibo_data',charset='utf8mb4')
cursor = conn.cursor()

for i in range(len(data)):
    page = (data.iloc[i]['页码'])
    id = (data.iloc[i]['id'])
    author = (data.iloc[i]['微博作者'])
    time = (data.iloc[i]['发布时间'])
    text = (data.iloc[i]['微博内容'])
    zf = (data.iloc[i]['转发数'])
    pl = (data.iloc[i]['评论数'])
    dz = (data.iloc[i]['点赞数'])
    fb = (data.iloc[i]['发布于'])
    ipc = (data.iloc[i]['ip属地_城市'])
    ipp = (data.iloc[i]['ip属地_省份'])
    ipn = (data.iloc[i]['ip属地_国家'])
    url = (data.iloc[i]['url链接'])
    weight = (data.iloc[i]['权重'])
    emo = (data.iloc[i]['情感'])
    avgemo = (data.iloc[i]['平均情感'])
    na = (data.iloc[i]['目标国家'])
    print(page,id,author,time,text,zf,pl,dz,fb,ipc,ipp,ipn,url,weight,emo,avgemo,na)
    sql = "INSERT INTO sumup(页码,id,微博作者,发布时间,微博内容,转发数,评论数,点赞数,发布于,ip属地_城市,ip属地_省份,ip属地_国家,url链接,权重,情感,平均情感,目标国家) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # try:
    cursor.execute(sql,(page,id,author,time,text,zf,pl,dz,fb,ipc,ipp,ipn,url,weight,emo,avgemo,na))
    conn.commit()
    #     print('write')
    # except:
    #     conn.rollback()
    #     print('failed')
cursor.close()
conn.close()

# CREATE TABLE sum (页码 int,id int,微博作者 text,发布时间 text,微博内容 text,转发数 int,评论数 int,点赞数 int,发布于 text,ip属地_城市 text , ip属地_省份 text , ip属地_国家 text , url链接 text,权重 double,情感 double,平均情感 double,目标国家 text);