# 该代码用于查看关键字段
import linecache

filename = r'test2.trs'
filename2 = r'D:\数据库导出TRS文件\liebiao_final_1.trs'

def read_file(filename):
    with open(filename, 'r',encoding='gb18030') as file:
        # text = linecache.getline(file, 1)
        # print(text)
        i = 0
        for line in file:
            print(line)
            i+=1
            if i>=100:
                break

read_file(filename2)

#IR_EXPORTNAME;IR_EXPORTID;IR_EXPORTTYPE;IR_DELEOPERATOR;IR_DELETIME;IR_PUBTYPE;IR_ISTRASH;IR_SRESERVED3;IR_SRESERVED2;IR_SRESERVED1;IR_VRESERVED4;IR_VRESERVED3;IR_VRESERVED2;IR_VRESERVED1;IR_NRESERVED3;IR_NRESERVED2;IR_NRESERVED1;IR_STATUS;IR_WCMID;IR_URLBODY;IR_URLSIZE;IR_CHARSET;IR_FORMAT;IR_MIMETYPE;IR_URLLEVEL;IR_PAGERANK;IR_PAGELEVEL;IR_BBSKEY;IR_BBSTOPIC;IR_BBSNUM;IR_URLCONTENT;IR_URLTABLE;IR_URLIMAGE;IR_CONTENT;IR_DOCLENGTH;IR_TABLEFLAG;IR_IMAGEFLAG;IR_SIMRANK;IR_SIMFLAG;IR_ABSTRACT;IR_KEYWORDS;IR_CATALOG2;IR_CATALOG1;IR_CATALOG;IR_DISTRICT;IR_AUTHORS;IR_SRCNAME;IR_LOADTIME;IR_URLTIME;IR_URLDATE;IR_LASTTIME;IR_URLTOPIC;IR_URLTITLE;IR_GROUPNAME;IR_CHANNEL;IR_SITENAME;IR_EXTNAME;IR_URLNAME;IR_PKEY;IR_SERVICEID;IR_STARTID;IR_HKEY;IR_SID