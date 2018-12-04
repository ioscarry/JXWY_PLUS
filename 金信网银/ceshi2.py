import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; rv:1.7.3) Gecko/20040913 Firefox/0.10',
}
url = 'http://www.baidu.com'

rsp = requests.get(url,headers=headers)
print(rsp.request.headers)