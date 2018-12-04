import requests

# 构建url
url = 'https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn=50'
# 构建请求头
headers = {

}
# 遍历url

# 发送请求

# 储存文件

class tieba(object):
    def __init__(self,name,page):
        self.name = name
        self.base_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(name)
        # self.base_url = 'https://tieba.baidu.com/f?kw=%s&ie=utf-8&pn='%name
        self.url_list = [self.base_url + str(x*50) for x in range(page)]
        self.headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"

        }

    def get_data(self,url):
        res = requests.get(url,headers=self.headers)
        return res.content

    def save_data(self,data,index):
        file_name = self.name + str(index) + '.html'

        with open(file_name,'wb') as f:
            f.write(data)

    def run(self):
        # 构建url列表
        # 构建请求头
        # 遍历url列表

        for url in self.url_list:
            # 发送请求获取响应
            data = self.get_data(url)

            index = self.url_list.index(url)+1
            # 写文件保存
            self.save_data(data,index)

if __name__ == '__main__':
    a = tieba('帝吧', 3)
    a.run()