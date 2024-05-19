import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn import preprocessing
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
mpl.rcParams['axes.unicode_minus'] = False 

print(os.getcwd())

keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
overall_list=[]
for keyword in keyword_list:
    data = pd.read_csv('..\data\emo\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    list_weight_emo = data['情感'].to_list()
    overall_list = overall_list + list_weight_emo   

for keyword in keyword_list:
    scaler = preprocessing.MinMaxScaler()
    data = pd.read_csv('..\data\emo\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    l = len(data)
    list_weight_emo = data['情感'].to_list()
    normalized_list = scaler.fit_transform(np.array(list_weight_emo).reshape(-1,1))
    plt.boxplot(list_weight_emo)
    plt.title('微博网民对于{}态度直方图'.format(keyword))
    plt.text(5,1,'有效样本{}条'.format(l))
    plt.xlabel('{}'.format(keyword))
    plt.ylabel('微博数量')
    # plt.show()
    plt.savefig('../img/box_fig_{}.png'.format(keyword))
    plt.cla()
