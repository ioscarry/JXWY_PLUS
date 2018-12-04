import json
import re
import requests
from lxml import etree


class Toutiao(object):

    def __init__(self):
        self.url = 'http://www.gsdata.cn/rank/ajax_toutiao?&page=1'
        # self.url = 'http://www.gsdata.cn/rank/toutiao'
        self.header = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',

            'Referer': 'http://www.gsdata.cn/rank/toutiao',
            'X-Requested-With': 'XMLHttpRequest',

        }

        self.file = open('qingbozhishu.json','w')

    def run_data(self,url):
        res = requests.get(url=url,headers=self.header)
        return res.content.decode()

    def parse_data(self,data):
        data_n = json.loads(data)['data']

        a = re.findall('<h1><a class="color-blue" target="_blank" href="http://www.toutiao.com/">(.*)</a></h1>',data_n)
        b = re.findall('<td><span class="num-span">(\d+)</span></td>',data_n)
        c = re.findall('<td>(.*)</td>',data_n)
        list = []
        for i in c:
            if 'class' in i:
                continue
            else:
                list.append(i)

        list_n = []
        from pycparser.ply.cpp import xrange
        for i in xrange(0, len(list), 6):
            list_n.append(list[i:i + 6])
        # print(list_n)

        list_parse = []
        for i,x,q in zip(a,b,list_n):
            dict = {}
            dict['name'] = i
            dict['num'] = x
            dict['article_number'] = q[0]
            dict['reading_total'] = q[1]
            dict['reading_average'] = q[2]
            dict['comment_total'] = q[3]
            dict['comment_average'] = q[4]
            dict['TGR'] = q[5]
            list_parse.append(dict)
            print(dict)

        return list_parse

    def save(self,data):

        for i in data:
            data_json = json.dumps(i) + ',\n'
            self.file.write(data_json)

    def run(self):
        url = self.url
        data = self.run_data(url)
        parse_data = self.parse_data(data)
        self.save(parse_data)
        for i in range(2,59):
            url_n = 'http://www.gsdata.cn/rank/ajax_toutiao?&page={}'.format(i)
            data = self.run_data(url_n)
            parse_data = self.parse_data(data)
            self.save(parse_data)


if __name__ == '__main__':
    tou = Toutiao()
    tou.run()
