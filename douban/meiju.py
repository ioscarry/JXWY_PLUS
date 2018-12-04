import json
import os

import requests

class Douban(object):
    def __init__(self):
        self.base_url='https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?&start={}&count=18'
        self.offset = 0
        self.headers={
            'User_Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36',
            'Referer': 'https: // m.douban.com / movie / subject / 26887174 / vendors?from=subject',
        }
        # if not os.path.exists('meiju_.json'):
        #     self.file = open('meiju_.json','w')
        self.file = open('meiju_.json','w')


    def get_data(self,url):
        resp=requests.get(url,headers=self.headers)
        return resp.content.decode()

    # 处理数据,转成python类型
    def parse_data(self,data):
        dict_data = json.loads(data)
        tv_list = dict_data["subject_collection_items"]
        # 查看源码,遍历电视剧列表,拿到每部剧的title和url
        data_list = []
        for tv in tv_list:
            temp = {}
            temp['title'] = tv['title']
            temp['url'] = tv['url']
            data_list.append(temp)

        return data_list

    # 解析完之后保存数据
    def save_data(self,data_list):
        for data in data_list:
            json_data = json.dumps(data,ensure_ascii=False)
            self.file.write(json_data + ',\n')

    def __del__(self):
        self.file.close()

    def run(self):
        while True:
            url = self.base_url.format(self.offset)
            data = self.get_data(url)
            data_list = self.parse_data(data)
            print(data_list)
            self.save_data(data_list)
            self.offset += 18
            if data_list == []:
                break

if __name__ == '__main__':
    douban = Douban()
    douban.run()
