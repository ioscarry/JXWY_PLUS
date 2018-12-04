import requests


class xiecheng(object):
    def __init__(self):
        # 首页的url
        self.url = 'http://36kr.com/'
        self.headers = {
            'User_Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / '
                          '537.36(KHTML, likeGecko) Chrome / 65.0.3325.181Safari / 537.36',
            # 'Host':'vacations.ctrip.com',
            'Referer': 'http://vacations.ctrip.com/morelinetravel/p7856296s1.html?kwd=%e5%9b%9b%e5%b7%9d'
        }
        self.file = open('xiecheng.json','w',encoding='utf-8')
        # 往下翻页的url
        self.base_url = 'http://vacations.ctrip.com/bookingnext/Comment/Search?pkg=7856296&destEname=&districtID=0&country=0&urlCategory=morelinetravel&PMPicture=https://dimg04.c-ctrip.com/images/300f0n000000ehcb65338.jpg&pageIndex=3&score=undefined&IsTourGroupProduct=1'
        self.offset = 2

    def get_data(self,url):
        resp = requests.get(url,headers=self.headers)
        print(resp.content.decode())

    def run(self):
        url = self.base_url
        self.get_data(url)

if __name__ == '__main__':
    xx = xiecheng()
    xx.run()