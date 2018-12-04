import requests

url = 'http://www.baidu.com'
resp = requests.get(url)
cookiejar = resp.cookies
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
print(resp)
print(cookiejar)
print(type(cookiejar))
print('----------')
print(cookiedict)
print(type(cookiedict))

url = 'https://www.12306.cn/mormhweb/'
resp = requests.get(url,verify=False)
# resp = requests.get(url)
print(resp.content)