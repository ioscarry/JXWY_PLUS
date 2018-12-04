# 找群主购买 my_app_key, myappsecret, 以及蚂蚁代理服务器的 mayi_url 地址和 mayi_port 端口
import hashlib
import time

import requests

my_app_key = "1203595"
app_secret = "0961510fdecb9239f0024456211224a8"
mayi_url = 's3.proxy.mayidaili.com'
mayi_port = '9064'

# 蚂蚁代理服务器地址
mayi_proxy = {'http': 'http://{}:{}'.format(mayi_url, mayi_port)}
print(mayi_proxy)

# 准备去爬的 URL 链接
url = 'http://www.lua8.com/ip.php'

# 计算签名
timesp = '{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
print(timesp)
codes = app_secret + 'app_key' + my_app_key + 'timestamp' + timesp + app_secret
print(codes)
sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()
print(sign)

# 拼接一个用来获得蚂蚁代理服务器的「准入」的 header (Python 的 concatenate '+' 比 join 效率高)
authHeader = 'MYH-AUTH-MD5 sign=' + sign + '&app_key=' + my_app_key + '×tamp=' + timesp

# 用 Python 的 Requests 模块。先订立 Session()，再更新 headers 和 proxies
s = requests.Session()
s.headers.update({'Proxy-Authorization': authHeader})
s.proxies.update(mayi_proxy)
pg = s.get(url, timeout=(300, 270))  # tuple: 300 代表 connect timeout, 270 代表 read timeout
pg.encoding = 'UTF-8'
print(pg.text)
print('222.128.174.87')