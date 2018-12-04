import requests
from lxml import etree
import time
from queue import Queue
import threading

class Qiubai(object):
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()
        # self.len_queue=Queue()


    def get_url_list(self):
        for i in range(1,14):
            self.url_queue.put(self.temp_url.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url,headers=self.headers)
            print(response.status_code)
            if response.status_code == 503:
                self.url_queue.put(url)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            div_list = html.xpath('//div[@id="content-left"]/div')
            content_list = []
            for div in div_list:
                item = {}
                item['user_name'] = div.xpath('.//h2/text()')[0].strip()
                item['content'] = ''.join([i.strip() for i in div.xpath('.//div[@class="content"]/span/text()')])
                content_list.append(item)
            self.content_list_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_list_queue.get()
            for content in content_list:
                print(content)
            # self.len_queue.put(len(content_list))
            self.content_list_queue.task_done()

    def run(self):
        thread_list = []
        # 1.url_list
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)
        # 2.遍历,发送请求
        for i in range(3):  # 设置三个线程发送请求
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)

        # 3.提取数据
        t_content = threading.Thread(target=self.get_content)
        thread_list.append(t_content)
        # 4.保存
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)

        for t in thread_list:
            t.setDaemon(True)  # 守护主线程
            t.start()

        for q in [self.url_queue,self.html_queue,self.content_list_queue]:
            q.join() # 主线程等待队列结束

        print('主线程结束')


if __name__ == '__main__':
    t1 = time.time()
    qiubai = Qiubai()
    qiubai.run()
    print('总时间:',time.time()-t1)