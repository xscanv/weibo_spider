import os
import re  
from jsonpath import jsonpath  
import requests  
import pandas as pd  
import datetime  

headers = {
	"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
}


def trans_time(v_str):
	GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
	timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
	ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
	return ret_time


def getLongText(v_id):
	url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
	r = requests.get(url, headers=headers)
	json_data = r.json()
	long_text = json_data['data']['longTextContent']
	dr = re.compile(r'<[^>]+>', re.S)
	long_text2 = dr.sub('', long_text)
	return long_text2


def get_weibo_list(v_keyword, v_max_page):
	for page in range(2, v_max_page + 1):
		print('===Page {} Processing==='.format(page))
		url = 'https://m.weibo.cn/api/container/getIndex'
		params = {
			"containerid": "100103type=1&q={}".format(v_keyword),
			"page_type": "searchall",
			"page": page
		}
		r = requests.get(url, headers=headers, params=params)
		if(r.status_code==200):
			cards = r.json()["data"]["cards"]
			print(len(cards),' card found')
			region_name_list = []
			status_city_list = []
			status_province_list = []
			status_country_list = []
			url_list=[]
			for card in cards:
				url_list.append(url)
				try:
					region_name = card['card_group'][0]['mblog']['region_name']
					region_name_list.append(region_name)
				except:
					region_name_list.append('')
				try:
					status_city = card['card_group'][0]['mblog']['status_city']
					status_city_list.append(status_city)
				except:
					status_city_list.append('')
				try:
					status_province = card['card_group'][0]['mblog']['status_province']
					status_province_list.append(status_province)
				except:
					status_province_list.append('')
				try:
					status_country = card['card_group'][0]['mblog']['status_country']
					status_country_list.append(status_country)
				except:
					status_country_list.append('')
			text_list = jsonpath(cards, '$..mblog.text')
			dr = re.compile(r'<[^>]+>', re.S)
			text2_list = []

			if not text_list:  
				continue
			if type(text_list) == list and len(text_list) > 0:
				for text in text_list:
					text2 = dr.sub('', text) 
					text2_list.append(text2)
			time_list = jsonpath(cards, '$..mblog.created_at')
			time_list = [trans_time(v_str=i) for i in time_list]
			author_list = jsonpath(cards, '$..mblog.user.screen_name')
			id_list = jsonpath(cards, '$..mblog.id')
			isLongText_list = jsonpath(cards, '$..mblog.isLongText')
			idx = 0
			for i in isLongText_list:
				if i == True:
					long_text = getLongText(v_id=id_list[idx])
					text2_list[idx] = long_text
				idx += 1
			reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
			comments_count_list = jsonpath(cards, '$..mblog.comments_count')
			attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')

			df = pd.DataFrame(
				{
					'页码': [page] * len(id_list),
					'微博id': id_list,
					'微博作者': author_list,
					'发布时间': time_list,
					'微博内容': text2_list,
					'转发数': reposts_count_list,
					'评论数': comments_count_list,
					'点赞数': attitudes_count_list,
					'发布于': region_name_list,
					'ip属地_城市': status_city_list,
					'ip属地_省份': status_province_list,
					'ip属地_国家': status_country_list,
					'url':url_list
				}
			)
			if os.path.exists(v_weibo_file):
				header = None
			else:
				header = ['页码', 'id', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数', '发布于','ip属地_城市','ip属地_省份','ip属地_国家','url链接']  
			df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')




keyword_list=['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国']
for keyword in keyword_list:
	if __name__ == '__main__':
		page_num = 10 
		search_keyword = keyword
		v_weibo_file = 'weibo_key={}_pgs={}.csv'.format(search_keyword, page_num)
		if os.path.exists(v_weibo_file):
			os.remove(v_weibo_file)
		get_weibo_list(v_keyword=search_keyword, v_max_page=page_num)
		df = pd.read_csv(v_weibo_file)
		df.drop_duplicates(subset=['id'], inplace=True, keep='first')
		path='C:/Users/26514/Desktop/v_weibo_file_{}.csv'.format(search_keyword)
		df.to_csv(path, index=False, encoding='utf_8_sig')
		print('Done:spider for {}'.format(search_keyword))