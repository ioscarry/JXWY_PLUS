import re

def readTrs(filePath):

    with open(filePath, 'rb') as file:
        content = file.readlines()
        everyStr = ""
        dicContent = {}
        for line in content:
            line = line.decode('gb18030').strip()
            everyStr += line
            if "<IR_SID>=" in everyStr and "<REC>" in everyStr:

                dicContent["SID"] = re.search("<IR_SID>=(.*)", everyStr).group(1)
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
            print(dicContent)

filePath = r'test.trs'
readTrs(filePath)