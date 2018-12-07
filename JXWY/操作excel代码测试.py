import xlrd,xlwt,openpyxl
from xlutils.copy import copy

# 一般xlrd读取原excel文件内容，通过xlwt新建excel文件并写入；
# 若想对原excel文件读写操作，需要xlutils的copy函数，或直接使用openpyxl；
'=================================   xlrd   =========================================='
def use_xlrd():
    readbook = xlrd.open_workbook('mix.xls',formatting_info=True) # 保留原格式
    sheet = readbook.sheet_by_name('Sheet1') # 此时sheet是对象
    # sheet = readbook.sheet_by_index(0)  或  readbook.sheets()[0]

    # 获取sheet最大行数和列数
    nrows = sheet.nrows #行
    ncols = sheet.ncols #列

    # 获取整行和整列的值（数组）
    nrows_values = sheet.row_values(0)
    ncols_values = sheet.col_values(0)
    print(nrows_values)
    print(ncols_values)
    # 获取单元格的值
    lng = sheet.cell(1,1).value  # 获取2行2列的表格值 ,从0开始
    print(lng)

'=================================   xlwt 只能新建表并写入内容  =========================================='
def use_xlwt():
    # 打开新表并添加sheet
    writebook = xlwt.Workbook() #打开一个excel
    sheet = writebook.add_sheet('test') #在打开的excel中添加一个sheet
    # 在sheet的单元格中写入内容
    sheet.write(0,0,'hehe')  #()
    writebook.save('test.xls')  # 一定要记得保存

'=================================   xlwt 通过copy进行操作  =========================================='
def use_copy(file_name,*sheet_name):
    rb = xlrd.open_workbook(file_name,formatting_info=True,) # 保留原数据格式
    rs = rb.sheet_by_index(0)
    wb = copy(rb)         # 复制原文件
    ws = wb.get_sheet(0)  # 复制后文件的第一个sheet；

    # 获取原sheet最大行数和列数
    nrows = rs.nrows  # 行
    ncols = rs.ncols  # 列
    print(nrows,type(nrows))
    print(ncols,type(ncols))

    # 尝试获取copy后的行数列数，不知道出来的字典什么玩意
    rowNum = ws.rows  # 行数
    colNum = ws.cols  # 无数据，空字典
    print(rowNum,type(rowNum))
    print(colNum,type(colNum))
    for i in rowNum:
        print(i)
    print('------------------------------------')
    # for index in rowNum:
    #     if index == 0:
    #         print(row)
    #         ws.write(index, 0, 'hehe') # （行，列，值）
    #     else:
    #         ws.write(index, 2, 'bqqm.com')
    wb.save(file_name)
    print('增加了一列')

'=================================   openpyxl  =========================================='
def use_openpyxl(name):
    wb = openpyxl.load_workbook(name) # 读文件
    ws = wb.worksheets[0]     # 选sheet
    sheets = wb.sheetnames
    # ws = wb.get_sheet_by_name(sheetnames[0])
    print(sheets)
    for i in sheets:
        print(i)

    # 获取最大行数和列数
    rows = ws.max_row  # 获取表的行数
    cols = ws.max_column  # 获取表的列数
    print(rows,cols)

    # 获取单元格的值
    lng = ws.cell(1, 1).value   # 从1开始，而不是从0开始
    print(lng,type(lng))
    # lat = ws.cell(row = i+1,column = 5).value
    lng = 'hehe' # 可直接赋值

    # 在第3列之前插入一列
    ws.insert_cols(3)
    # 填入数据
    for index, row in enumerate(ws.rows):
        if index == 0:
            row[2].value = 'ceshi'
        else:
            row[2].value = 'hello'
    wb.save(name)

    # # 通过openpyxl创建新文件
    # outwb = openpyxl.Workbook()
    # outws = outwb.create_sheet(title='test_openpyxl')
    # for i in range(rows):
    #     lng = ws.cell(row=i + 1, column=4).value  # 读文件
    #     lat = ws.cell(row=i + 1, column=5).value
    #     outws.cell(row=i + 1, column=1).value = lng  # 写文件
    #     outws.cell(row=i + 1, column=2).value = lat
    # outwb.save('out.xlsx')

'=================================   csv  =========================================='
if __name__ == '__main__':

    filename_xlsx = r'D:\工作文件\项目\pachong_practice\金信网银\ailaba.xlsx'
    filename_xls = ''
    file_csv = ''
    use_openpyxl('jqw.xlsx')