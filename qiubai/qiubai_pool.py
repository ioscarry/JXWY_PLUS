import requests
from lxml import etree
import time
from queue import Queue
from multiprocessing.dummy import Pool

class Qiubai(object):
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        self.queue = Queue()
        self.pool = Pool(7)
        self.is_running = True
        self.total_requests_num = 0
        self.total_response_num = 0

    def get_url_list(self):
        for i in range(1,14):    # 使用url队列, 线程池中的线程自动处理任务,相互协作
            self.queue.put(self.temp_url.format(i))
            self.total_requests_num += 1

    def parse_url(self,url):
        response = requests.get(url,headers=self.headers)
        print(response.status_code)
        # if response.status_code == 503:
        #     self.queue.put(url)
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
        # return len(content_list)

    def exetute_requests_item_save(self):  # 将所有流程汇总在一起成一个函数
        url = self.queue.get()
        html_str = self.parse_url(url)
        content_list = self.get_content(html_str)
        self.save_content_list(content_list)
        self.total_response_num += 1
        # self.queue.task_done()

    def _callback(self,temp):
        if self.is_running:
            self.pool.apply_async(self.exetute_requests_item_save,callback=self._callback)


    def run(self):
        self.get_url_list()
        for i in range(2):    #控制并发,此处控制2个.
            self.pool.apply_async(self.exetute_requests_item_save,callback=self._callback)

        while True: # 防止主线程结束
            # time.sleep(0.001)  # 避免cpu空转
            if self.total_response_num >= self.total_requests_num:
                self.is_running = False
                break

        # url_list = self.get_url_list()
        # a = 0
        # for url in url_list:
        #     html_str = self.parse_url(url)
        #     content = self.get_content(html_str)
        #     self.save_content_list(content)
        #     a += self.save_content_list(content)
        # print(a)


if __name__ == '__main__':
    t1 = time.time()
    qiubai = Qiubai()
    qiubai.run()
    print('总时间:',time.time()-t1)