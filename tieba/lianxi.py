import requests
import json

class Spider(object):
    def __init__(self,name):
        self.name = name
        self.url = 'http://www.163.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"

        }

    def get_data(self,url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self,data):
        dict_data = json.loads(data,ensure_ascii=False)
        return dict_data

    def save_data(self,data):
        file_name = self.name + '.html'
        with open(file_name,'wb') as f:
            f.write(data)

    def __del__(self):
        pass

    def run(self):
        url = self.url
        data = self.get_data(url)
        # data = self.parse_data(data)
        self.save_data(data)

if __name__ == '__main__':
    spider = Spider('163')
    spider.run()