import requests
import json

import sys


class Spider(object):
    def __init__(self,word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            'User-Agent': "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit "
                          "/ 537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36",
        }
        self.post_data = {
            "f": "auto",
            "t": "auto",
            "w": word
        }

    def get_data(self,url):
        response = requests.post(url, headers=self.headers,data=self.post_data)
        return response.content.decode()

    def parse_data(self,data):
        dict_data = json.loads(data)
        print(dict_data)
        try:
            result = dict_data['content']['word_mean'][0]
        except:
            result = dict_data['content']['out'][0]
        return result

    def save_data(self,data):
        pass

    def __del__(self):
        pass

    def run(self):
        url = self.url
        data = self.get_data(url)
        result = self.parse_data(data)
        print(result)

if __name__ == '__main__':
    word = sys.argv[1]
    spider = Spider(word)
    spider.run()