import numpy as np
import pandas as pd
import os
print (os.getcwd()) 

sum_up=1
keyword_list=['阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
for keyword in keyword_list:
    data = pd.read_csv('..\data\emo\weibo_key={}_pgs=50_emoscore.csv'.format(keyword))
    list1 = []
    list2 = []
    sample_num = len(data)
    for i in range (0,sample_num):
        list1.append(data.iloc[i, 14]/len(data.iloc[i, 4]))
        list2.append(keyword)
    data1 = pd.DataFrame({"目标国家":list2})
    data2 = pd.DataFrame({"平均情感": list1})
    data = pd.concat([data, data2 ,data1], axis=1)
    if sum_up:
        sum=data
        sum_up=0
    else:
        sum=pd.concat([sum,data],axis=0,join='inner')
sum.to_csv('..\data\sum\sum_emoscore.csv', index=False, encoding='utf_8_sig')
print(sum)