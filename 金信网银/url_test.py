import json
import random
import time

import requests

# url = 'http://www.baidu.com'

file = open('bianmin.json','w')

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

def request(url):
    resp = requests.get(url, headers = headers)
    print(resp.status_code)
    print(resp.url)
    data = {}
    data['url'] = url
    if resp.url == url:
        data['status_code'] = resp.status_code
    else:
        data['status_code'] = 404
    # data['status_code'] = resp.status_code
    json_data = json.dumps(data, ensure_ascii=False)
    file.write(json_data + ',\n')

def delay():
    delay = random.randint(0, 2)
    time.sleep(delay)

url_list = open('url.txt','r')
for i in url_list.readlines():
    request(i.strip())
    delay()



url_list.close()
file.close()
print('检测完毕')