import dump_load
import requests
import sys


class King(object):
    # 设置请求头,url, 请求参数
    def __init__(self,word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit "
                          "/ 537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36"
        }
        self.post_data = {
            "f": "auto",
            "t": "auto",
            "w": word
        }

    # 发送请求取得数据
    def get_data(self):
        res = requests.post(url=self.url,headers=self.headers,data=self.post_data)
        return res.content.decode()

    # 解析数据
    def parse_data(self,data):
        # 将json字符串转换为python字典
        dict_data = dump_load.loads(data)
        try:
            result = dict_data['content']['out']
        except:
            result = dict_data['content']['word_mean']

        print(type(dict_data))
        print(result)

    def run(self):
        data = self.get_data()
        self.parse_data(data)

if __name__ == '__main__':
    # word = input('想查啥:')
    # a = King(word)
    # print(type(a.get_data()))
    # print(a.get_data())
    # a.run()

    # print(sys.argv)
    word = sys.argv[1]
    king = King(word)
    king.run()