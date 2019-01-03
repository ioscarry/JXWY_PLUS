# 以迭代对象遍历的方式进行处理， 读取每一项，当遇到关键字段yield返回
# 使用前先确定关键字段！！！！！！！
# 该代码使用之前需对照asc进行更新

import re
import time

filename = r'test.trs'
filename2 = r'C:\Users\zhd\Desktop\liebiao_2.trs'
begin = time.time()
final_count = 0
erro_count = 0
dicContent = {}  # 以字典格式存储每一条数据
mix_list = []    # 汇总到列表

def read_file(filename):
    with open(filename, 'r',encoding='gb18030') as file:
        allStr = ""    # 将所有内容拼接到一起
        for line in file:
            allStr += line.strip()
            if 'IR_SID'in line:
                yield allStr
                allStr = ""

# for循环解析迭代对象的字符串
# i = 0
for everyStr in read_file(filename):
    final_count += 1
    print(everyStr)
    # i += 1
    # if i >= 10:
    #     break
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
    mix_list.append(dicContent)

    print('-------------------------------------------------------------')
    '=====================================华丽的分割线============================================'

print(time.time()-begin)
print('处理数据的数量：' + str(final_count))
print(len(mix_list))