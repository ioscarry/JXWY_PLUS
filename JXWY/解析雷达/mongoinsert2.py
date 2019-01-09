# 以迭代对象遍历的方式进行处理， 读取每一项，当遇到关键字段yield返回
# 使用前先确定关键字段！！！！！！！

import re
import time
from pymongo import MongoClient

# client = MongoClient(host='127.0.0.1', port=27018, userName='lizehua', password='lizehua')
client = MongoClient(host='192.168.2.99', port=27018)
print(client.address)
print(client.list_database_names())
# db = client.JXWY
db = client.hehe
print(db.list_collection_names())
col = db['jxwy']
# col = db['test']
# col.remove({})
#192.168.2.253 27017

filename = r'test.trs'
filename2 = r'D:\云服务器导出TRS文件\lieju266572.trs'

begin = time.time()
final_count = 0
erro_count = 0
erro_list = []    # 报错汇总到列表

def read_file(name):
    with open(name, 'rb') as file:
        allStr = ""    # 将所有内容拼接到一起
        try:
            for line in file:
                line = line.decode('gb18030', 'ignore')
                allStr += line.strip()
                if 'IR_PUBTYPE' in line:
                    yield allStr
                    allStr = ""
        except Exception as e:
            erro_list.append(str(final_count+1)+ str(e) + ',\n')
            print(e)

def start():
    global final_count,erro_count
    for everyStr in read_file(filename2):
        final_count += 1
        # if final_count > 10:
        #     break
        print(final_count)
        dicContent = {}  # 以字典格式存储每一条数据
        '=====================================华丽的分割线============================================'
        try:
            dicContent["SID"] = re.search("<IR_SID>=(.*?)<IR_HKEY>", everyStr).group(1)
            dicContent["urlname"] = re.search("<IR_URLNAME>=(.*?)<IR_.+?>=", everyStr).group(1)
            dicContent["updatetime"] = re.search("<IR_LASTTIME>=(.*?)<IR_.+?>=", everyStr).group(1).replace(".", "-")
            dicContent["urltime"] = re.search("<IR_URLTIME>=(.*?)<IR_.+?>=", everyStr).group(1).replace(".", "-")
            dicContent["urltitle"] = re.search("<IR_URLTITLE>=([\s\S]*?)<IR_.+?>=", everyStr).group(1)
            dicContent["category"] = re.search("<IR_CHANNEL>=(.*?)<IR_.+?>=", everyStr).group(1)
            dicContent["fuwu"] = re.search("<IR_CHANNEL>=(.*?)<IR_.+?>=", everyStr).group(1)
            dicContent["sitename"] = re.search("<IR_SITENAME>=(.*?)<IR_.+?>=", everyStr).group(1)

            try:
                dicContent["province"] = re.search("<IR_VRESERVED1>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["province"] = ""

            try:
                dicContent["city"] = re.search("<IR_VRESERVED2>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["city"] = ''
            try:
                dicContent["content"] = re.search("<IR_CONTENT>=([\s\S]*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["content"] = ""

            try:
                dicContent["company"] = re.search("<IR_SRCNAME>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["company"] = ""

            try:
                dicContent["address"] = re.search("<IR_DISTRICT>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["address"] = ""

            if re.search("<IR_SRESERVED1>=(.*?)<IR_.+?>=", everyStr) != None:
                dicContent["yuming"] = re.search("<IR_SRESERVED1>=(.*?)<IR_.+?>=", everyStr).group(1)
            else:
                dicContent["yuming"] = ''

            if re.search("<IR_VRESERVED3>=(.*?)<IR_.+?>=", everyStr) != None:
                dicContent["icp"] = re.search("<IR_VRESERVED3>=(.*?)<IR_.+?>=", everyStr).group(1)
            else:
                dicContent["icp"] = ''

            try:
                dicContent["icpsheng"] = re.search("<IR_VRESERVED4>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["icpsheng"] = ''

            try:
                dicContent["people"] = re.search("<IR_AUTHORS>=(.*?)<IR_.+?>=", everyStr).group(1)
            except:
                dicContent["people"] = ''
        except:
            erro_count += 1
            print('这条数据不正常')

        print(dicContent)

        # col.update({"urlname":dicContent["urlname"]},dicContent, upsert=True)  # 条件存在则修改，无则新建插入
        # col.insert_one(dicContent)
        # col.update_one({'urlname':dicContent["urlname"]},{'$setOnInsert':dicContent},upsert=True)  # 条件存在则pass，无则新建插入

if __name__ == '__main__':
    start()
    print('=====================================华丽的分割线============================================')
    print('处理的时长为：'+str(time.time()-begin))
    print('处理数据的数量：' + str(final_count))
    print('插入失败的数量：' + str(erro_count))
    print('------------')
    print('数据库该集合的数据量：'+ str(col.estimated_document_count()))
    print(erro_list)