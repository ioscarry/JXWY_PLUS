import requests

PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

proxy = get_proxy()
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy,
}
try:
    response = requests.get('http://www.baidu.com',proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error',e.args)