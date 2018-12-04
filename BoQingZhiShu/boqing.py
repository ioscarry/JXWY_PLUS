#coding:utf-8

import json
import re
import requests
from lxml import etree

from selenium import webdriver

class BOQING(object):
    def __init__(self):
        self.url = 'http://www.gsdata.cn/rank/ajax_toutiao?type=week&post_time=20180604_20180610&gid=1&page=2'
        self.headers = {
            'User_Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / '
                          '537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36',
            'Cookie':'myad=1; bdshare_firstime=1529484744902; _gsdataCL=WzEzOTIyNiwiMTgwMzc5MDU4MTUiLCIyMDE4MDYyMDE3MTAzNiIsImJmMDU3Nzc4ZThkMDNiYzhhMDcxMTk5NGIyZmFkZjllIiwxMTgwNjRd; _identity-frontend=e6bdfaccff1874a6540f1e3158c46d9b3833dc30e6b07652dc57f04001fdd01aa%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B139226%2C%22test+key%22%2C2592000%5D%22%3B%7D; acw_tc=AQAAALLMbk2K2A0AEnCCDsxb5K3Nt764; PHPSESSID=q6dtrcl52hju00njvvpgrqa8d2; _csrf-frontend=7aabc313bd6da472fb2a067bc7f2105b83afdbdf2fc8c8883812cd45822eca88a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22ao7NbDJHCTQHwpJjw4jkrP-weFBoKRDw%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1529484745,1529493141; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1529493141',
            'Host':'www.gsdata.cn',
        }
        # self.file = open('boqing.json','w')
        # opt = webdriver.ChromeOptions()
        # opt.add_argument('headless')
        # # 创建浏览器配置对象
        # driver = webdriver.Chrome()

    def get_data(self,url):

        url = self.url
        # driver.get(url)
        # el_sub = driver.find_elements_by_xpath('//a[@id="add_data"]')
        # el_sub.click()
        resp = requests.get(url,headers=self.headers)
        return resp.content

    def parse_data(self,data):
        html = etree.HTML(data)
        node_list = html.xpath('//table[@id="rank_data"]/tbody/tr')
        # results = re.findall('<a target="_blank" href="(.*?)">(.*?)</a>',data)
        print(type(node_list))
        data_list = []
        for node in node_list:
            temp = dict()
            temp['rank'] = node.xpath('./td[1]/span/text()')[0]
            temp['name'] = node.xpath('./td[2]/div/div/h1/a/text()')[0]
            temp['public'] = node.xpath('./td[3]/text()')[0]
            temp['total_read'] = node.xpath('./td[4]/text()')[0]
            temp['avg_read'] = node.xpath('./td[5]/text()')[0]
            temp['total_comment'] = node.xpath('./td[6]/text()')[0]
            temp['avg_comment'] = node.xpath('./td[7]/text()')[0]
            temp['TGI'] = node.xpath('./td[8]/text()')[0]

            data_list.append(temp)

        print(len(data_list))

        # 获取下一页
        next_url = html.xpath('//*[@id="add_data"]')
        return data_list,next_url
    #
    # def save_data(self,data_list):
    #     # with open('guoke.json','w')as f:
    #     #     for data in data_list:
    #     #         json_data = json.dumps(data,ensure_ascii=False) + ',\n'
    #     #         f.write(json_data)
    #     for data in data_list:
    #         json_data = json.dumps(data) + ',\n'
    #         self.file.write(json_data)
    #
    # def __del__(self):
    #     self.file.close()
    #
    def run(self):
        url = self.url
        data = self.get_data(url)
        data_list = self.parse_data(data)

        # self.save_data(data_list)



if __name__ == '__main__':
    boqing=BOQING()
    boqing.run()