#coding=utf-8
import json
import re

import requests


class ke36(object):
    def __init__(self):
        # 首页的url
        self.url = 'http://36kr.com/'
        self.headers = {
            'User_Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / '
                          '537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36',
        }
        self.file = open('36kr.json','w',encoding='utf-8')
        # 往下翻页的url
        self.base_url = 'http://36kr.com/api/search-column/mainsite?per_page=20&page={}'
        self.offset = 2

    def get_data(self,url):
        resp = requests.get(url,headers=self.headers)
        return resp.content.decode()

    def parse_data(self,data):  # 处理首页数据
        json_data = re.findall('<script>var props=({.*?})</script>',data)[0]
        json_data = json_data.split(',locationnal=')[0]
        print(type(json_data))

        # with open('temp1.json','w',encoding='utf-8')as f:
        #     f.write(json_data)
    #     # 将json数据转换成python字典
    #     dict_data = json.loads(json_data)

    #     # 取到特定板块的新闻标题和url
    #     news_list = dict_data["feedPostsLatest|post"]
    #
    #     data_list = []
    #     for news in news_list:
    #         temp = dict()
    #         temp['title'] = news['title']
    #         temp['url'] = news['cover']
    #         data_list.append(temp)
    #
    #     return data_list
    #
    # def save_data(self,data_list):
    #     for data in data_list:
    #         json_data = json.dumps(data,ensure_ascii=False) + ',\n'
    #         self.file.write(json_data)
    #
    # def parse_ajax_data(self,data):
    #     dict_data = json.loads(data)
    #
    #     news_list = dict_data['data']['items']
    #
    #     data_list = []
    #     for news in news_list:
    #         temp = dict()
    #         temp['title'] = news['title']
    #         temp['url'] = news['cover']
    #         data_list.append(temp)
    #
    #     return data_list
    #
    # def __del__(self):
    #     self.file.close()
    #
    def run(self):
        url = self.url
        data = self.get_data(url)
        data_list=self.parse_data(data)
    #     self.save_data(data_list)
    #
    #     # 循环获取下页新闻
    #     while True:
    #         # 构建ajaxurl
    #         url = self.base_url.format(self.offset)
    #         # 发送请求
    #         data = self.get_data(url)
    #         # 解析
    #         data_list = self.parse_ajax_data(data)
    #         # 保存
    #         self.save_data(data_list)
    #         # 判断是否结尾
    #         if data_list == []:
    #             break
    #         # 模拟翻页
    #         self.offset += 1


if __name__ == '__main__':
    ke = ke36()
    ke.run()