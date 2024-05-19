import os
from os import path
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import jieba

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
mpl.rcParams['axes.unicode_minus'] = False 
font = r'C:\Users\26514\Desktop\SimHei.ttf'

keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']

stopwords_list=['网页链接']

for keyword in keyword_list:
    data = pd.read_csv('.\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    sample_num = len(data)
    text=''
    for i in range(sample_num):
        text = text + data.iloc[i, 4]
    wordlist = list(jieba.cut(text)) 
    wordlist = [word for word in wordlist if len(word)>1]
    wordlist = " ".join(wordlist)
    wordcloud = WordCloud(background_color='white',font_path=font,stopwords=stopwords_list).generate(text)
    print(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title('{}相关微博词云图'.format(keyword))
    plt.savefig('./img/cloud_fig_{}.png'.format(keyword))
    plt.cla()


