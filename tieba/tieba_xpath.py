import os

from lxml import etree

import requests
import json

class Spider(object):
    def __init__(self,name):
        self.name = name
        self.url = 'https://tieba.baidu.com/f?kw={}'.format(self.name)
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)',
        }

    def get_data(self,url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self,data):
        # 将响应内容创建成element对象,由XPath获取标签
        html = etree.HTML(data)
        node_list = html.xpath('//*/li[@class=" j_thread_list clearfix"]/div/div/div[1]/div[1]/a')
        # print(node_list)
        # print(len(node_list))

        detail_list = []
        for node in node_list:
            temp = {}
            temp['title'] = node.xpath('./text()')[0]
            temp['url'] = 'https://tieba.baidu.com' + node.xpath('./@href')[0]
            detail_list.append(temp)

        next_url = html.xpath('//a[@class="next pagination-item"]/@href')
        return detail_list,next_url

    def parse_detail_page(self,page):
        # 解析详情页,获取图片数据
        html = etree.HTML(page)   # 解析HTML文档. 以用来在Python代码中嵌入“HTML文字”。
        pic = html.xpath('//*[contains(@id,"post")]/img/@src')
        return pic

    def download(self,image_list):
        if not os.path.exists('pic'):
            os.makedirs('pic')
        for url in image_list:
            imag = self.get_data(url)
            imag_name = 'pic'+ os.sep + url.split('/')[-1]
            with open(imag_name,'wb') as f:
                f.write(imag)


    def run(self):
        url = self.url
        while True:
            data = self.get_data(url)
            with open('temp.html','wb') as f:
                f.write(data)
            detail_list, next_url = self.parse_data(data)
            # 遍历列表发起详情页请求
            for detail in detail_list:
                # print(detail['url'])
                page = self.get_data(detail['url'])
                # 解析详情页面响应获取图片url列表
                image_list = self.parse_detail_page(page)
                # print(image_list)
                self.download(image_list)

            # 若贴吧没有下一页,停止循环
            if next_url == []:
                break
            else:
                url = 'https:' + next_url[0]


if __name__ == '__main__':
    spider = Spider('绿巨人')
    spider.run()