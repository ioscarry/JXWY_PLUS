
# 该代码为检测url的有效性，适用于若失效返回404的情况

import json
import random
import time

import requests

class Ceshi(object):

    def __init__(self):
        self.file = open('ailaba.json','a+')
        # self.file2 = open('ailaba.json','r')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.list = []
        self.final = 0

    def request(self,url):
        resp = requests.get(url, headers = self.headers)
        print(resp.status_code)
        print(resp.url)
        data = {}
        # 判断是否遇到反爬，如果遇到就不加入到json文件中
        if ('spider'or'redirect') in resp.url:
            self.final += 1
        else:
            data['url'] = url
            # if resp.url == url:
            #     data['status_code'] = resp.status_code
            # else:
            #     data['status_code'] = 404
            data['status_code'] = resp.status_code
            data['domain'] = 'ailaba.com'
            json_data = json.dumps(data, ensure_ascii=False)
            self.file.write(json_data + ',\n')

    def delay(self):
        delay = random.random()+1
        time.sleep(delay)

    def judge_url(self):
        content = self.file.readlines()
        for i in content:
            ins = i.strip().strip(',')
            t = json.loads(ins)
            self.list.append(t['url'].strip())

    def __del__(self):
        self.file.close()
        # self.file2.close()

if __name__ == '__main__':
    ceshi = Ceshi()
    ceshi.judge_url()
    with open('url.txt', 'r') as url_list:
        for i in url_list.readlines():
            if i.strip() not in ceshi.list:
                ceshi.request(i.strip())
                ceshi.delay()

    print('检测完毕')
    print('遇到的反爬数量为' + str(ceshi.final))