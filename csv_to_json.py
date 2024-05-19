import json
import os

# print(os.getcwd())

keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
for keyword in keyword_list:
    data = open('..\data\emo\weibo_key={}_pgs=50_emoscore.csv'.format(keyword),"r",encoding='utf-8')
    ls=[]
    for line in data:
        line=line.replace("\n","")
        ls.append(line.split(","))
    data.close()
    name = 'weibo_key={}_pgs=50_emoscore.json'.format(keyword)
    fw = open(name,"w",encoding='utf-8')
    for i in range(1,len(ls)):
        ls[i]=dict(zip(ls[0],ls[i]))
    json_data = json.dumps(ls[1:],sort_keys=True,indent=4,ensure_ascii=False)
    # print(json_data)
    fw.write(json_data)
    fw.close()
