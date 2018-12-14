# 一次性处理， 卡爆

import re,time
filename = r'test.trs'
filename2 = r'C:\Users\zhd\Desktop\liebiao_2.trs'

begin = time.time()
with open(filename, 'r',encoding='gb18030') as file:

    allStr = ""    # 将所有内容拼接到一起
    dicContent = {}  # 以字典格式存储每一条数据
    mix_list = []    # 汇总到列表
    # print(type(content))
    # print(content)

    for line in file:
        allStr += line.strip()

    allReg = re.findall(r'<REC>.*?<IR_PUBTYPE>',allStr)
    # print(allReg[0])
    print('----------------------------------------------------------')
    for everyStr in allReg:
        print(everyStr)
        dicContent["SID"] = re.search("<IR_SID>=(.*?)<IR_HKEY>", everyStr).group(1)
        dicContent["urlname"] = re.search("<IR_URLNAME>=(.*?)<IR_.+?>=", everyStr).group(1)
        dicContent["loadtime"] = re.search("<IR_LASTTIME>=(.*?)<IR_.+?>=", everyStr).group(1).replace(".", "-")
        dicContent["updatatime"] = dicContent["loadtime"]
        dicContent["urltime"] = re.search("<IR_URLTIME>=(.*?)<IR_.+?>=", everyStr).group(1).replace(".", "-")
        dicContent["urltitle"] = re.search("<IR_URLTITLE>=([\s\S]*?)<IR_.+?>=", everyStr).group(1)
        dicContent["category"] = re.search("<IR_CHANNEL>=(.*?)<IR_.+?>=", everyStr).group(1)
        dicContent["fuwu"] = re.search("<IR_CHANNEL>=(.*?)<IR_.+?>=", everyStr).group(1)

        if re.search("<IR_VRESERVED1>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["province"] = re.search("<IR_VRESERVED1>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["province"] = ""

        if re.search("<IR_VRESERVED2>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["city"] = re.search("<IR_VRESERVED2>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["city"] = ''
        if re.search("<IR_CONTENT>=([\s\S]*?)<IR_.+?>=", everyStr) != None:
            dicContent["content"] = re.search("<IR_CONTENT>=([\s\S]*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["content"] = ""

        if re.search("<IR_SRCNAME>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["company"] = re.search("<IR_SRCNAME>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["company"] = ""

        if re.search("<IR_DISTRICT>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["address"] = re.search("<IR_DISTRICT>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["address"] = ""

        dicContent["sitename"] = re.search("<IR_SITENAME>=(.*?)<IR_.+?>=", everyStr).group(1)

        if re.search("<IR_SRESERVED1>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["yuming"] = re.search("<IR_SRESERVED1>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["yuming"] = ''

        if re.search("<IR_VRESERVED3>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["icp"] = re.search("<IR_VRESERVED3>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["icp"] = ''

        if re.search("<IR_VRESERVED4>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["icpsheng"] = re.search("<IR_VRESERVED4>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["icpsheng"] = ''

        if re.search("<IR_AUTHORS>=(.*?)<IR_.+?>=", everyStr) != None:
            dicContent["people"] = re.search("<IR_AUTHORS>=(.*?)<IR_.+?>=", everyStr).group(1)
        else:
            dicContent["people"] = ''

        print('-------------------------------------------------------------')
        print(dicContent)
        mix_list.append(dicContent)

    print(time.time() - begin)
    print(mix_list)
    print(len(mix_list))