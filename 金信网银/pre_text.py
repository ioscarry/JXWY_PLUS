
# 该代码用于在检测之前对网站返回的内容进行分析

import random
import time
import requests

class test_url(object):

    def __init__(self):
        # self.file = open('liebiao.json','w')
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.0; rv:1.7.3) Gecko/20040913 Firefox/0.10',
        }

    def request(self,url):
        resp = requests.get(url, headers = self.headers)
        # resp = requests.get(url,headers = self.headers,proxies={'http':'http://1203595:0961510fdecb9239f0024456211224a8@s3.proxy.mayidaili.com:9064'})
        print(resp.status_code)
        print(resp.url)
        print(resp.encoding)
        print(resp.apparent_encoding)
        print(requests.utils.get_encodings_from_content(resp.text))
        # print(resp.content.decode(resp.encoding))

        if resp.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(resp.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = resp.apparent_encoding
            # global encode_content
            encode_content = resp.content.decode(encoding, 'replace')#.encode('utf-8', 'replace') #如果设置为replace，则会用?取代非法字符；
            print(encode_content)
        else:
            print(resp.text)


        # print(resp.request.headers)
        # data = {}
        # data['url'] = url
        # data['status_code'] = resp.status_code
        # json_data = json.dumps(data, ensure_ascii=False)
        # file.write(json_data + ',\n')

    def delay(self):
        delay = random.random()+1
        time.sleep(delay)

    def run(self):
        url_list = open('url.txt','r')
        for i in url_list.readlines():
            self.request(i)
            self.delay()
        # url_list.close()
        # file.close()
        print('检测完毕')

if __name__ == '__main__':
    # url = 'http://wuhan.kuyiso.com/daikuan/33989681x.htm'
    url = 'http://www.jqw.com/proshow-2017000195250.htm'

    t = test_url()
    t.request(url)