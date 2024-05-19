import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
mpl.rcParams['axes.unicode_minus'] = False 

keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
overall_list=[]
for keyword in keyword_list:
    data = pd.read_csv('.\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    list_weight_emo = data['情感'].to_list()
    overall_list = overall_list + list_weight_emo   
upper=np.percentile(overall_list, 98)
lower=np.percentile(overall_list, 2)
range=(lower,upper)

color_dict={'中国':'#FF0000','阿根廷':'#7CB0DF','澳大利亚':'#003469','巴西':'#336F1B','加拿大':'#FF0000','法国':'#0055A4','德国':'#FFCE00','印度':'#656C12','印度尼西亚':'#FF0000','意大利':'#008C45','日本':'#EA4D72','韩国':'#293380','墨西哥':'#006341','俄罗斯':'#46C7FF','沙特阿拉伯':'#B09255','南非共和国':'#FF8400','土耳其':'#A4795E','英国':'#1251B0','美国':'#6F0119'}

for keyword in keyword_list:
    scaler = preprocessing.MinMaxScaler()
    data = pd.read_csv('.\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    l = len(data)
    list_weight_emo = data['情感'].to_list()
    normalized_list = scaler.fit_transform(np.array(list_weight_emo).reshape(-1,1))
    plt.hist(list_weight_emo,range=range,bins=100,color=color_dict[keyword])
    plt.title('微博网民对于{}态度直方图'.format(keyword))
    plt.text(5,1,'有效样本{}条'.format(l))
    plt.xlabel('微博情绪')
    plt.ylabel('微博数量')
    # plt.show()
    plt.savefig('./img/hist_fig_{}.png'.format(keyword))
    plt.cla()
