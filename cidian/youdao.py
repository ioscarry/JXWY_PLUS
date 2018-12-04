import hashlib
import random

import requests
import json
import time

class Youdao(object):
    def __init__(self,word):
        self.word = word
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1190431479@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=914799038.6754858; JSESSIONID=aaanut7NNGdRZ8e0Oa5ow; NTES_SESS=Utu4jxpS1RcIkIv2jbHIjcGhksG48rFVk7E.HJW14tTADJLIDjktuVin1dfxbxECTgUR7xA92wRELyy_Gz24LRtD37RM2Fmqnxwm97JhNGmapMHmPJVYlznCN3F4QmAIad2SRN_nzvYb0GFTDIG3iM7FprdJ9ZTEtd8mbUqTdHYhK.FwXBm0AopZNXuoO8xAeeRjzy3ji_p93cOAh1._P.onsnqdVClK9; ANTICSRF=1ed43886b61f062b6b719349f19c9068; S_INFO=1528187483|0|3&80##|m13911775903_1; P_INFO=m13911775903_1@163.com|1528187483|0|other|00&99|bej&1526284460&other#bej&null#10#0#0|139903&1|mail163|13911775903@163.com; ___rl__test__cookies=1528292261216'
        }
        self.post_data = None

    def generate_post_data(self):
        # 构造r
        # r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
        now = int(time.time()*1000) # salt是13位,时间戳是10位,所以小数点后挪3位
        randint = random.randint(0,9)
        r = str(now + randint)
        # 构造o
        # o = u.md5(S + n + r + D)    # md5是哈希运算的一种
        S = "fanyideskweb"
        n = self.word
        D = "ebSeFb%=XZ%T[KZ)c(sy!"

        tempstr = S + n + r + D
        # # 1 构建hash对象
        md5 = hashlib.md5()
        # # 2 将需要进行hash运算的字符串更新到hash对象中, python3中需要bytes类型的字符串数据
        md5.update(tempstr.encode())
        # # 3 获取字符串对应的hash值
        o = md5.hexdigest()

        self.post_data = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": r,
            "sign": o,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTIME",
            "typoResult": False,
        }

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        return response.content.decode()

    def parse_data(self, data):
        dict_data = json.loads(data,encoding='utf-8')
        print(dict_data)

    def run(self):
        # url = self.url
        # data = self.get_data(url)
        # self.parse_data(data)
        self.generate_post_data()
        data = self.get_data()
        # 解析相应
        self.parse_data(data)

if __name__ == '__main__':
    youdao = Youdao('china')
    youdao.run()