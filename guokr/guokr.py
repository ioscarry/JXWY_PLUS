#coding:utf-8

import json
import re

import requests

#  <a target="_blank" href="https://www.guokr.com/question/668948/">子弹能射穿多少本书，与那一摞书本的本数多少有何关系？</a>

class Guokr(object):
    def __init__(self):
        self.url = 'https://www.guokr.com/ask/highlight/?page=1'
        self.headers = {
            'User_Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / '
                          '537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36',

        }
        self.file = open('guokr2.json','w')

    def get_data(self,url):
        resp = requests.get(url,headers=self.headers)
        return resp.content.decode()

    def parse_data(self,data):
        # dict_data = json.loads(data)
        results = re.findall('<a target="_blank" href="(.*?)">(.*?)</a>',data)

        data_list = []
        for result in results:
            url = result[0]
            title = result[-1]
            if 'class' in url:
                continue

            temp = dict()
            temp['title'] = title
            temp['url'] = url
            data_list.append(temp)

        # 获取下一页
        next_url = re.findall('<a href="(/ask/highlight/\?page=\d+)">下一页</a>',data)
        return data_list,next_url

    def save_data(self,data_list):
        # with open('guoke.json','w')as f:
        #     for data in data_list:
        #         json_data = json.dumps(data,ensure_ascii=False) + ',\n'
        #         f.write(json_data)
        for data in data_list:
            json_data = json.dumps(data) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()

    def run(self):
        url = self.url
        while True:
            data = self.get_data(url)
            data_list,next_url = self.parse_data(data)
            self.save_data(data_list)

            if next_url == []:
                break
            # 构建下一页url
            url = 'https://www.guokr.com' + next_url[0]

if __name__ == '__main__':
    guoke=Guokr()
    guoke.run()