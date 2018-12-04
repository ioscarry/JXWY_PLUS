
# 该代码为检测url的有效性，适用于若失效返回200的情况，需从源码内容进行判断，并考虑到不同页面的编码问题。

import json
import random
import time
import requests

class Ceshi(object):

    def __init__(self):
        self.file = open('qidian8.json','a+')
        self.file2 = open('qidian8.json','r')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.list = []  # 将json文件中的url存放到list中备用做判断
        self.final = 0

    def request(self,url):
        resp = requests.get(url, headers = self.headers,proxies={'http':'http://1203595:0961510fdecb9239f0024456211224a8@s3.proxy.mayidaili.com:9064'})
        print('原状态码：'+ str(resp.status_code))
        print(resp.url)
        data = {}
        # 考虑到ip被监测到为爬虫的情况就不记录到json文件，当程序跑完在控制台提示是否被反。（案例：百姓网）
        if ('spider'or'redirect') in resp.url:
            self.final += 1
        else: # 没被检测到爬虫，进入正常页面进行解析
            if resp.status_code == 200:
                # 考虑到不同编码格式问题，需要根据请求头的编码信息进行解析
                if resp.encoding == 'ISO-8859-1':
                    encodings = requests.utils.get_encodings_from_content(resp.text)
                    if encodings:
                        encoding = encodings[0]
                    else:
                        encoding = resp.apparent_encoding
                    # global encode_content
                    encode_content = resp.content.decode(encoding,'replace')  # .encode('utf-8', 'replace') #如果设置为replace，则会用?取代非法字符；
                else:
                    encode_content = resp.text
                if '您要访问的页面不存在' in encode_content:    # 具体分析每个失效页面内容的特点，若没有该特点可判断为正常页面
                    data['status_code'] = 404
                else:
                    data['status_code'] = 200
            else:
                data['status_code'] = resp.status_code    # 记录除200以外的状态码

            # data['status_code'] = resp.status_code
            print('处理后的status:'+ str(data['status_code']))
            data['url'] = url
            data['domain'] = 'kuyiso.com'
            json_data = json.dumps(data, ensure_ascii=False)
            self.file.write(json_data + ',\n')

    def delay(self):
        delay = random.random()+1
        time.sleep(delay)

    def judge_url(self):
        content = self.file2.readlines()
        # print(content)
        for i in content:
            ins = i.strip().strip(',')
            t = json.loads(ins)
            self.list.append(t['url'].strip())
        # print(self.list)

    def __del__(self):
        self.file.close()
        self.file2.close()

if __name__ == '__main__':
    ceshi = Ceshi()
    ceshi.judge_url()
    with open('url2.txt', 'r') as url_list:
        for i in url_list.readlines():
            if i.strip() not in ceshi.list:
                ceshi.request(i.strip())
                ceshi.delay()

    print('检测完毕')
    print('遇到的反爬数量为' + str(ceshi.final))