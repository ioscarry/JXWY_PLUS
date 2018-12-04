import requests
from lxml import etree
import time
from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue

class Qiubai(object):
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        for i in range(1,2):
            self.url_queue.put(self.temp_url.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            html_str = requests.get(url,headers=self.headers)
            print(html_str.status_code)
            self.html_queue.put(html_str.content.decode())
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

            self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            for content in content_list:
                print(content)
            self.content_queue.task_done()

    def run(self):
        process_list = []
        # 1.url_list
        t_url = Process(target=self.get_url_list)
        process_list.append(t_url)
        # 2.遍历,发送请求
        for i in range(1):
            t_pase = Process(target=self.parse_url)
            process_list.append(t_pase)
        # 3.提取数据
        t_content = Process(target=self.get_content)
        process_list.append(t_content)
        # 4.保存
        t_save = Process(target=self.save_content_list)
        process_list.append(t_save)

        for t in process_list:
            t.daemon=True # 把进程设置为守护进程, 子进程随主进程结束
            t.start()
        for q in [self.url_queue,self.html_queue,self.content_queue]:
            q.join()  # 让主进程阻塞

        print('主进程结束')


if __name__ == '__main__':
    t1 = time.time()
    qiubai = Qiubai()
    qiubai.run()
    print('总时间:',time.time()-t1)