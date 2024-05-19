import pandas as pd
import os
import numpy as np
import jieba
from sklearn import preprocessing

#基于波森情感词典计算情感值
def getscore(text):
    df = pd.read_table(".\Desktop\weibo\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    # jieba分词
    segs = jieba.lcut(text,cut_all = False) #返回list
    # 计算得分
    score_list = [score[key.index(x)] for x in segs if(x in key)]
    return sum(score_list)

keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
for keyword in keyword_list:
    data = pd.read_csv('.\Desktop\weibo\weibo_key={}_pgs=50.csv'.format(keyword))
    scaler = preprocessing.MinMaxScaler()
    sample_num = len(data)
    list1 = data['转发数'].to_list()
    list2 = data['评论数'].to_list()
    list3 = data['点赞数'].to_list()

    normalizedlist1 = scaler.fit_transform(np.array(list1).reshape(-1,1))
    normalizedlist2 = scaler.fit_transform(np.array(list2).reshape(-1,1))
    normalizedlist3 = scaler.fit_transform(np.array(list3).reshape(-1,1))

    total_list = normalizedlist1 + normalizedlist2 + normalizedlist3
    total_list = total_list*10/3
    data.insert(data.shape[1], '权重', total_list)
    sentiment = []
    for i in range (0,sample_num):
        if (data.iloc[i, 10]!=data.iloc[i, 10]):
            data.iloc[i, 10]=data.iloc[i, 11]
        if (data.iloc[i, 9]!=data.iloc[i, 9]):
            data.iloc[i, 9]=data.iloc[i, 10]
    for i in range (0,sample_num):
        text = data.iloc[i, 4]
        score = getscore(text)*(data.iloc[i, 13]+15)
        sentiment.append(score)
        print(i,'of',sample_num,'for',keyword)
    data.insert(data.shape[1], '情感', sentiment)
    path = '.\Desktop\weibo\emo'
    if os.path.exists('weibo_key=中国_pgs=50_emoscore.csv'):
        os.remove('weibo_key=中国_pgs=50_emoscore.csv')
    data.to_csv('.\Desktop\weibo\weibo_key={}_pgs=50_emoscore.csv'.format(keyword), index=False, encoding='utf_8_sig')

