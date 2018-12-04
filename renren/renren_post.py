import requests

url = 'http://www.renren.com/PLogin.do'

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

post_data = {
    'email':'616236330@qq.com',
    'password':'169598479'
}

# 发送请求,模拟登陆
session = requests.Session()
session.post(url,headers=headers,data=post_data)
# 使用session请求数据
response = session.get('http://www.renren.com')

print(response.content.decode())