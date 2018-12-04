import time
import xlwt, json, openpyxl,xlrd
from xlutils.copy import copy
#
# def readJsonfile():
#     jsobj = json.load(open(r'C:\Users\zhd\Desktop\项目\pachong_practice\金信网银\liebiao.json'))
#     return jsobj

def readJsonfile(file_path):
    with open(file_path) as j:
        return j.readlines()
    # for i in f:
    #     d = json.loads(i.strip().strip(','))
    #     print(d,type(d))

def jsonToexcel(file_name,sheet_name):
    jsonfile = readJsonfile(file_path)
    print(jsonfile)
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(sheet_name)  # 创建表名
    ll = list(json.loads(jsonfile[0].strip().strip(',')).keys())    # 设置表头：获取json文件中的keys，并转化为list
    for i in range(0, len(ll)):             # 将list中的keys设置成表头
        sheet1.write(0, i, ll[i])           # 向excel中写入数据(行号，列号，值)
    for j in range(0, len(jsonfile)):
        m = 0
        ls = list(json.loads(jsonfile[j].strip().strip(',')).values())
        for k in ls:
            sheet1.write(j + 1, m, k)       # 向excel中写入数据(行号，列号，值)
            m += 1
    workbook.save(file_name)           # 添加完之后保存数据
    print('已从json导出到excel')


def addcol_xlsx(name):
    wb = openpyxl.load_workbook(name)
    ws = wb.worksheets[0]
    # 在第3列之前插入一列
    ws.insert_cols(3)
    # 填入数据
    for index, row in enumerate(ws.rows):
        if index == 0:
            row[2].value = 'domain'
        else:
            row[2].value = 'bqqm.com'
    wb.save(name)

def addcol_xls(file_name,sheet_name):
    rb = xlrd.open_workbook(file_name,formatting_info=True) # 保留原数据格式
    wb = copy(rb)
    ws = wb.get_sheet(0)  #取第一个sheet ,sheet_by_index(0)
    # ws = rb.sheet_by_name(sheet_name)

    rowNum = ws.rows
    colNum = ws.cols
    for index, row in enumerate(rowNum):
        if index == 0:
            ws.write(index, 2, 'domain') # （行，列，值）
        else:
            ws.write(index, 2, 'bqqm.com')
    wb.save(file_name)
    print('增加了一列')

if __name__ == '__main__':
    file_path = r'C:\Users\zhd\Desktop\项目\pachong_practice\金信网银\jqw.json'
    print(readJsonfile(file_path))

    file_name = 'jqw.xls'
    sheet_name = 'jqw.com'

    jsonToexcel(file_name,sheet_name)
    # addcol_xls(file_name,sheet_name)