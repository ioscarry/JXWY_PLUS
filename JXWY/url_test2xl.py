# 该代码为检测url的有效性，适用于若失效仍会返回200的情况.

# 测试直接从excel操作,并将结果写入excel文件新增列中
# 1. 读取excel中的url；
# 2. 新增两列，根据对url的检测结果进行标注(响应url和状态码) -------------------  可以优化；
# 3. 检测机制基本完善， 实现功能：
# #         1.判断请求url与返回url的一致性；
# #         2.从源码内容进行判断；
# #         3.考虑到不同页面的编码问题；
# #         4.检测完一遍进行第二次检测补漏时会自动对url排重，不再请求已经访问过的url

# 在第二次检测时需要将新增两行的代码注释掉！！！！！！！！！！

import random
import time,openpyxl
import requests

class Ceshi(object):

    def __init__(self,text):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.final = 0
        self.count = 0
        self.text = text

    def request(self, url):
        resp = requests.get(url, headers=self.headers, proxies={})
        print('原状态码：' + str(resp.status_code))
        print(resp.url)
        # 考虑到ip被监测到为爬虫的情况就不记录到文件，当程序跑完在控制台提示是否被反。（案例：百姓网）
        if ('spider' or 'redirect') in resp.url:
            self.final += 1
            return

        else:  # 若没被检测到爬虫，进入正常页面进行解析；
            # 先考虑状态码为200的情况；
            if resp.status_code == 200:
                # 若状态吗为200，判断返回的url与请求的url是否一致；
                if resp.url != url:
                    status_code = 404
                # 若url一致，则判断源码内容，需考虑到不同编码格式问题，需要根据请求头的编码信息进行解析
                elif resp.encoding == 'ISO-8859-1':
                    encodings = requests.utils.get_encodings_from_content(resp.text)
                    if encodings:
                        encoding = encodings[0]
                    else:
                        encoding = resp.apparent_encoding
                    # global encode_content
                    self.encode_content = resp.content.decode(encoding,'replace')  # .encode('utf-8', 'replace') #如果设置为replace，则会用?取代非法字符；
                    status_code = self.judge_content()
                else:
                    self.encode_content = resp.text
                    status_code = self.judge_content()
            else:
                # 若状态码不是200，则直接记录200以外的状态码
                status_code = resp.status_code
            self.count += 1
            print('处理后的status:' + str(status_code))
            return (status_code,resp.url)

    def judge_content(self):
        if self.text in self.encode_content:  # 具体分析每个失效页面内容的特点，若没有该特点可判断为正常页面
            return 404
        else:
            return 200

    def delay(self):
        delay = random.random()
        time.sleep(delay)

def run(name,again,text):
    ceshi = Ceshi(text)
    wb = openpyxl.load_workbook(name)  # 读文件
    sheetnames = wb.sheetnames
    print(sheetnames)
    # ws = wb.worksheets[3]  # 选sheet
    # ws = wb.get_sheet_by_name(sheetnames[0])
    ws = wb['58']

    rows = ws.max_row  # 获取表的行数
    # cols = ws.max_column  # 获取表的列数
    '-------------------------------------------------------------'
    if again == 0:
        ws.insert_cols(4, 2) # 在第3列之前插入2列
    '-------------------------------------------------------------'
    # 获取单元格的值（url）并测试,将返回的url和status_code写入excel文件；
    for index in range(rows):
        url = ws.cell(index + 1, 3).value  # 顺序从1开始；
        judge_url = ws.cell(index + 1, 4)
        if judge_url.value:
            continue
        else:
            try:
                code, rsurl = ceshi.request(url)
            except:
                code, rsurl = None, None
            if code:
                judge_url.value = rsurl
                ws.cell(index + 1, 5).value = code
            else:
                continue
        ceshi.delay()

    # for index, row in enumerate(ws.rows):
    #     if index == 0:
    #         row[2].value = 'domain'
    #     else:
    #         row[2].value = 'bqqm.com'
    wb.save(name)

    print('检测完毕')
    print('共检测' + str(ceshi.count) + '条数据')
    print('遇到的反爬数量为' + str(ceshi.final))

if __name__ == '__main__':

    file_name = '20181205_监测源.xlsx'  # 在run方法里设置要操作的sheet
    check_again = 0  # 默认为0（新增两行），若再次检测需改为1(若有信息就不会检测).
    judge_text = '您浏览的页面不存在'
    run(name=file_name,again=check_again,text=judge_text)