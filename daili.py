import requests

proxies = {
    # 'http': 'http://121.234.53.207:61234',
    'https': 'https://118.67.218.197:8080',
}
headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

response = requests.get("http://www.baidu.com",headers = headers,proxies = proxies,timeout = 5)
# print (response.text)