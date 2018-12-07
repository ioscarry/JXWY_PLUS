import requests
from lxml import etree
import json
import threading
from queue import Queue

class Spider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        }
        # 创建url列表
        self.url_list = None
        # 创建文件保存数据
        self.file = open('qiushi2.json','w',encoding='utf-8')
        # 创建三个数据队列
        self.url_queue = Queue()
        self.res_queue = Queue()
        self.data_queue = Queue()


    def generate_url_list(self):
        # self.url_list = [self.base_url.format(i) for i in range(1,14)]
        for i in range(1,14):
            url = self.base_url.format(i)
            self.url_queue.put(url)

    def get_data(self):
        while True:
            url = self.url_queue.get()
            print('正在获取{}对应的响应'.format(url))
            response = requests.get(url, headers=self.headers)
            print(response.status_code)
            # 判断响应状态,如果503便将url放回队列
            if response.status_code == 503:
                self.url_queue.put(url)
            else:
                self.res_queue.put(response.content)
            self.res_queue.put(response.content)
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            data = self.res_queue.get()
            print('正在解析响应')
            # 构建element对象
            html = etree.HTML(data)

            # 获取所有帖子节点列表
            node_list = html.xpath('//*[contains(@id,"qiushi_tag_")]')
            # print(len(node_list))

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

            self.data_queue.put(data_list)
            self.res_queue.task_done()

    def save_data(self):
        while True:
            data_list = self.data_queue.get()
            print('正在保存数据')
            for data in data_list:
                str_data = json.dumps(data,ensure_ascii=False) + ',\n'
                self.file.write(str_data)
            self.data_queue.task_done()

    def __del__(self):
        self.file.close()

    def run(self):
        # self.generate_url_list()
        # for url in self.url_list:
        #     data = self.get_data(url)
        #     data_list = self.parse_data(data)
        #     print(data_list)
        #     self.save_data(data_list)

        # 创建多线程列表
        thread_list = []
        # 创建生成url列表的线程
        t_generate_url = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_generate_url)

        # 创建发送请求的线程
        for i in range(4):
            t = threading.Thread(target=self.get_data)
            thread_list.append(t)

        # 创建解析数据的线程
        for i in range(3):
            t = threading.Thread(target=self.parse_data)
            thread_list.append(t)

        # 创建保存数据的线程
        t_save_data = threading.Thread(target=self.save_data)
        thread_list.append(t_save_data)

        # 设置线程并开启线程
        for t in thread_list:
            # 设置守护线程
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue,self.res_queue,self.data_queue]:
            q.join()

if __name__ == '__main__':
    spider = Spider()
    spider.run()