#coding:utf-8
import requests
import dump_load
import sys

class King(object):

    def __init__(self, word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        self.post_data = {
            "f": "auto",
            "t": "auto",
            "w": word
        }

    def get_data(self):
        response = requests.post(url=self.url, headers=self.headers, data=self.post_data)
        return response.content.decode()

    def parse_data(self, data):
        # 将json字符串转换成python字典
        dict_data = dump_load.loads(data)

        try:
            result = dict_data['content']['out']
        except:
            result = dict_data['content']['word_mean']

        print(result)

    def run(self):

        # 构建url
        # 请求头
        # 构建post数据
        # 发送请求
        data = self.get_data()
        # 解析数据
        self.parse_data(data)

if __name__ == '__main__':
    word = sys.argv[1]
    king = King(word)
    king.run()
