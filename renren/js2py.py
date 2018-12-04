import requests
import json
import js2py

session = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type":"application/x-www-form-urlencoded"
}
url = 'http://activity.renren.com/livecell/rKey'
session.headers=headers
response = session.get(url)
# print(response.content.decode())
n = json.loads(response.content.decode())['data']
# print(n)

phoneNum = '18686702208'
password = '169598479'
# 使用js2py生成js的执行环境: context
context = js2py.EvalJs()
# 拷贝到本地然后读取操作,使用context来执行.
with open('BigInt.js','r',encoding='utf8')as f:
    context.execute(f.read())

with open('RSA.js','r',encoding='utf8') as f:
    context.execute(f.read())
with open('Barrett.js','r',encoding='utf8')as f:
    context.execute(f.read())

context.t = {'password':password}
context.n = n
