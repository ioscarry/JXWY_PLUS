# -*- coding: utf-8 -*-
import json

import re
import scrapy

from Qingbo.items import QingboItem


class QingboSpider(scrapy.Spider):
    name = 'qingbo'
    allowed_domains = ['gsdata.cn']
    start_urls = ['http://www.gsdata.cn/rank/toutiao']

    def parse(self, response):
        for i in range(1, 59):
            url = 'http://www.gsdata.cn/rank/ajax_toutiao?gid=1&page={}'.format(i)
            yield scrapy.Request(url, callback=self.parse_ajax, meta={'num': i})

    def parse_ajax(self, response):
        meta = response.meta['num']
        print(meta)
        # 定义模型
        item = QingboItem()
        data = response.body
        data_1 = json.loads(data)['data']
        data_2 = data_1.replace(' ', '')
        data_3 = data_2.replace('\r\n', '')

        teple_list = re.findall(
            r'">(\d+)</span></td><td><divclass="img-wordno-img"><divclass="word"><h1><aclass="color-blue"target="_blank"href="http://www.toutiao.com/">(\w+)</a></h1><spanclass=""></span></div></div></td><td>(\d+)</td><td>(.+?)</td><td>(\d+)</td><td>(\d+)</td><td>(\d+)</td><td>(.+?)</td>',
            data_3)
        for rank, title, publish_num, total_read_num, avg_read_num, total_comment_num, avg_comment_num, TGI in teple_list:
            item['rank'] = rank
            item['title'] = title
            item['publish_num'] = publish_num
            item['total_read_num'] = total_read_num
            item['avg_read_num'] = avg_read_num
            item['total_comment_num'] = total_comment_num
            item['avg_comment_num'] = avg_comment_num
            item['TGI'] = TGI
            yield item
