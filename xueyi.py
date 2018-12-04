import requests

url='https://www.baidu.com/s'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

data = input('guanjianzi:')
params = {
    "wd":data
}

response = requests.get(url,headers=headers,params=params)

print(response)

with open('xueyi.html','wb') as f:
    f.write(response.content)