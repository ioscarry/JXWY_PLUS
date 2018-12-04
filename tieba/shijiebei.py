import os

import requests
from lxml import etree

import requests
import json

class Spider(object):
    def __init__(self,name):
        self.name = name
        self.url = 'https://tieba.baidu.com/f?kw={}'.format(self.name)
        self.headers = {
            # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
        }

    def get_data(self,url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self,data):
        # 将响应内容创建成element对象,由XPath获取标签
        html = etree.HTML(data)
        node_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')
        detail_list = []
        for node in node_list:
            temp = {}
            temp['title'] = node.xpath('./text()')[0]
            temp['url'] = 'https://tieba.baidu.com' + node.xpath('./@href')[0]
            detail_list.append(temp)
        print(len(detail_list))

        next_url = html.xpath('//a[@class="next pagination-item"]/@href')
        return detail_list, next_url

    def parse_detail_data(self,detail_page):
        html = etree.HTML(detail_page)
        pic = html.xpath('//div[contains(@id,"post")]/img[@class="BDE_Image"]/@src')
        print(pic)
        print(type(pic))

        pic_list=[]
        # for p in pic:
        #     pic_list.append(p)
        pic_list.extend(pic)
        while True:
            try:
                detail_next_url = 'https://tieba.baidu.com' + html.xpath('//li[@class="l_pager pager_theme_5 pb_list_pager"]/a[contains(text(),"下一页")]/@href')[0]
            except:
                break
            next_page = self.get_data(detail_next_url)
            html = etree.HTML(next_page)
            pic = html.xpath('//div[contains(@id,"post")]/img[@class="BDE_Image"]/@src')
            # for p in pic:
            #     pic_list.append(p)
            pic_list.extend(pic)

        return pic_list

    def save_data(self,image_list):
        if not os.path.exists('pic_shijiebei'):
            os.makedirs('pic_shijiebei')
        for url in image_list:
            imag = self.get_data(url)
            imag_name = 'pic_shijiebei'+ '/' + url.split('/')[-1]
            with open(imag_name,'wb',) as f:
                f.write(imag)


    def run(self):
        url = self.url
        while True:
            data = self.get_data(url)
            detail_list, next_url = self.parse_data(data)
            for detail_page in detail_list:
                detail = self.get_data(detail_page['url'])
                # pic,detail_next_url = self.parse_detail_data(detail)
                pic_list = self.parse_detail_data(detail)
                self.save_data(pic_list)
                # if detail_next_url:
                #     detail_next_page = self.get_data(detail_next_url)
            if next_url:
                url = 'https:' + next_url[0]
            else:
                break

if __name__ == '__main__':
    spider = Spider('世界杯')
    spider.run()