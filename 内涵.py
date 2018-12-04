import requests
import re

class Duanzi_spider():
    def __init__(self):
        self.url = "http://www.neihan8.com/article/list_5_%s.html"
        self.headers = {
            "User_Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleW\
            ebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept-Encoding":None,
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "www.neihan8.com"

        }

    def load_page(self,url):
        '''可以复用的页面请求方法
        '''
        response = requests.get(url,timeout=10,headers=self.headers)
        if response.status_code==200:
            print(response.request.headers)
            return response.content.decode("gbk")
        else:
            raise ValueError("status_code is:",response.status_code)

    def get_content(self, html):
        '''  根据网页内容，同时匹配标题和段子内容
        '''
        pattern = re.compile(r'<a\shref="/article/\d+\.html">(.*?)</a>.*?<div\sclass="f18 mb20">(.*?)</div>', re.S)
        t = pattern.findall(html)
        result = []
        for i in t:
            temp = []
            for j in i:
                j = re.sub(r"[<b>|</b>|<br />|<br>|<p>|</p>|\\u3000|\\r\\n|\s]", "", j)
                j = j.replace("&ldqo;", '"').replace("&helli;", "...").replace("&dqo;", '"').strip()
                # j = re.sub(r"[&ldqo;|&dqo;]","\"",j)?
                # j = re.sub(r"…","...",j)
                temp.append(j)
            print(temp)
            result.append(temp)

        return result

    def run(self):
        i = 1
        while True:
            html = self.load_page(self.url % i)
            result = self.get_content(html)
            print("按回车继续...")
            print("输入 quit 退出")
            command = input()
            if (command == "quit"):
                break
            i += 1

if __name__ == '__main__':
    neihan = Duanzi_spider()
    neihan.run()
