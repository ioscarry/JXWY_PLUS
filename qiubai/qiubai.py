import requests
# XPath
from lxml import etree
import json

class Spider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        }
        # 创建url列表
        self.url_list = None
        # 创建文件保存数据
        self.file = open('qiushi.json','w',encoding='utf-8')

    def generate_url_list(self):
        self.url_list = [self.base_url.format(i) for i in range(1,14)]

    def get_data(self,url):
        print('正在获取{}对应的响应'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_data(self,data):
        print('正在解析响应')
        # 构建element对象
        html = etree.HTML(data)

        # 获取所有帖子节点列表
        node_list = html.xpath('//*[contains(@id,"qiushi_tag_")]')
        print(len(node_list))

        data_list = []
        # 遍历
        for node in node_list:
            temp = dict()
            try:
                temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()
                temp['link'] = 'https://www.qiushibaike.com' + node.xpath('./div[1]/a[2]/@href')[0]
                temp['age'] = node.xpath('./div[1]/div/text()')[0]
                temp['gender'] = node.xpath('./div[1]/div/@class')[0].split(' ')[-1].split('I')[0]
            except:
                temp['user'] = '匿名用户'
                temp['link'] = None
                temp['age'] = None
                temp['gender'] = None

            temp['content'] = ''.join([i.strip() for i in node.xpath('./a[1]/div/span/text()')])
            data_list.append(temp)

        return data_list

    def save_data(self,data_list):
        print('正在保存数据')
        for data in data_list:
            str_data = json.dumps(data,ensure_ascii=False) + ',\n'
            self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def run(self):
        self.generate_url_list()
        for url in self.url_list:
            data = self.get_data(url)
            data_list = self.parse_data(data)
            print(data_list)
            self.save_data(data_list)

if __name__ == '__main__':
    spider = Spider()
    spider.run()