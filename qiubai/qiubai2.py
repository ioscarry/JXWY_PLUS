import requests
from lxml import etree
import time

class Qiubai(object):
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }

    def get_url_list(self):
        return [self.temp_url.format(i) for i in range(1,14)]

    def parse_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_content(self,html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath('//div[@id="content-left"]/div')
        content_list = []
        for div in div_list:
            item = {}
            item['user_name'] = div.xpath('.//h2/text()')[0].strip()
            item['content'] = ''.join([i.strip() for i in div.xpath('.//div[@class="content"]/span/text()')])
            content_list.append(item)

        return content_list

    def save_content_list(self,content_list):
        for content in content_list:
            print(content)
        return len(content_list)

    def run(self):
        url_list = self.get_url_list()
        a = 0
        for url in url_list:
            html_str = self.parse_url(url)
            content = self.get_content(html_str)
            self.save_content_list(content)
            a += self.save_content_list(content)
        print(a)


if __name__ == '__main__':
    t1 = time.time()
    qiubai = Qiubai()
    qiubai.run()
    print('总时间:',time.time()-t1)