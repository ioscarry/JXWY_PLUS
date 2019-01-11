# coding=gbk
import sys,os

import pandas as pd
import datetime
import time

# df1=pd.DataFrame({'key':['b','b','a','a','b','a','c'],'data1':['A','B','C','D','E','F','G']})
#
# df2=pd.DataFrame({'key':['a','b','d'],'data2':['A','B','C']})
#
# print(pd.merge(df1,df2,on='key',how='outer'))

# t = datetime.datetime.now()
# print(t)
# temp = "2018-12-21 11:36:10"
# # af = time.strptime(temp, "%Y-%m-%d %H:%M:%S")
# print(datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S"))
# # print(af)
# print(temp[:7].replace('-',''))

# temp = {}
# temp['value'] = {}
# temp['value']['hehe'] = 5
# print(temp)

# from pymongo import MongoClient
# client = MongoClient('192.168.2.99', 27018)
# dbNew = client.hehe.company  #company库名
# # company = dbNew.aggregate([{$match:{"":}}])
# company = dbNew.find().limit(1)
# print(company)
# for i in company:
#     print(i)


t_time = "2018-12-02 15:26:57"
nian = t_time.split()
if '-' in nian[0]:
    t_nian = nian[0].split('-')
elif '.' in nian[0]:
    t_nian = nian[0].split('.')
if t_nian.__len__() != 3:
    a = time.strftime("%Y-%m-%d", time.localtime()).split()[0]
    a = a.split('-')
    t_nian = a
print(t_nian)

# def getADerInfo(name):
#     # company = cfg.dbNew
#     # company_d = {}
#     if len(str(name)) == 0:
#         company_d = {'important':"",'category': '','address': '', 'scope': '','num': ''}
#     else:
#         for item in range(3):
#             company_d = { 'important': 'haha'}
#     return company_d
#
# print(getADerInfo('hehe'))

a = time.strftime("%Y-%m-%d", time.localtime()).split()[0].split('-')
print(a)

law_data = 100
c1 = []
c2 = []
law_content = '|'.join(c2)
res={'law_real':'hehe','law_name':'haha','law_content':law_content}
if law_data > 0:
    if res['law_real'] is None:
        law_data -= 20
    if res['law_name'] is None:
        law_data -= 20
    if res['law_content'] is '':
        law_data -= 20

print(law_data)

a = None
b = ''
bb = 'hehe'
print('%s size is %d' %(type(a),sys.getsizeof(a)))
print('%s size is %d' %(type(b),sys.getsizeof(b)))
print('%s size is %d' %(type(bb),sys.getsizeof(bb)))

# dic = {'hehe':1,'xixi':2,'gege':3}
# print(sum(dic.values()))
# print(len(dic.keys()))

# print(os.system('cmd'))