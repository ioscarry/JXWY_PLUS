# -*- coding: utf-8 -*-

# to 协会广告生成csv
from pymongo import MongoClient
import pymongo
import csv
import out_config
import datetime

ad_address = out_config.address
ad_class = out_config.ad_class
e_class = out_config.e_class
filename = r"C:\Users\zhd\Desktop\To_jiaoyu.csv"
csvfile = open(filename, 'w', encoding='utf=8', newline='')
# writer = csv.writer(csvfile, delimiter='')
writer = csv.writer(csvfile)

client = MongoClient('192.168.2.99', 27018)
# 关键词和模型处理后的数据
final_adv_all = client.hehe.final_adv_all

def getlist(data):  # 将每条数据做进一步处理
    tmp = []
    keys = [
        'ad_id',
        'ad_loadTime',
        'ad_pushTime',
        'ad_url',
        'ad_title',
        'ad_category',
        'ad_KeyWords',
        'ad_numOfKeyWords',
        'ad_frequencyOfKeyWords',
        'ad_numOfContent',
        'ad_summary',
        'ad_content',
        'e_nameOfAdvertiser',
        'e_category',
        'e_address',
        'e_tag',
        'e_Scope',
        'e_num',
        'm_name',
        'm_yu',
        'm_icp',
        'm_tag',
        'm_address',
        'law_real',
        'law_name',
        'law_content',
        'law_picid',
        'other_terminal',
        'other_c_type',
        'other_b_num',
        'other_ip_num',
        'complete_index',
        'spread_index',
        'law_index',
        'venture_index',
        'level_venture',
        'version']

    for key in keys:
        if key == 'ad_loadTime' or key == 'ad_pushTime':
            tmp.append(data[key].replace('.', '-').split()[0])
        elif key == 'e_tag' or key == 'm_tag':
            tmp.append(str(data[key]))
        elif type(data[key]) is str:
            tmp.append(data[key].replace('\n', '@@@n@@@').replace('\r', '@@@r@@@'))
        else:
            tmp.append(data[key])
    return tmp

def getnewid(id):
    num = 6 - len(str(id))
    return '0' * num + str(id)

t_dit = {'version': "20181231", 'e_address': {'$nin': [None, '']}, 'law_real': {'$nin': [None, '']}}
#### 没有公司主体、没有地址的数据协会不要 ###
count = 0
ad_data = final_adv_all.find(t_dit).sort('venture_index', pymongo.DESCENDING)
print(ad_data)
for data in ad_data:
    print(data)
#   将数据库中满足要求的数据排序，然后遍历处理
    tmp = [data['ad_id'],
           data['ad_loadTime'].replace('.', '-'),
           data['ad_pushTime'].replace('.', '-'),
           data['ad_url'].replace('\n', '@@@n@@@').replace('\r', '@@@r@@@'),
           data['ad_title'].replace('\n', '@@@n@@@').replace('\r', '@@@r@@@'),
           data['ad_category'],
           data['ad_KeyWords'],
           data['ad_numOfKeyWords'],
           data['ad_frequencyOfKeyWords'],
           data['ad_numOfContent'],
           data['ad_summary'].replace('\n', '@@@n@@@').replace('\r', '@@@r@@@'),
           data['ad_content'].replace('\n', '@@@n@@@').replace('\r', '@@@r@@@'),
           data['e_nameOfAdvertiser'],
           data['e_category'],
           data['e_address'],
           data['e_tag'],
           data['e_Scope'],
           data['e_num'],
           data['m_name'],
           data['m_yu'],
           data['m_icp'],
           data['m_tag'],
           data['m_address'],
           data['law_real'],
           data['law_name'],
           data['law_content'],
           data['law_picid'],
           data['other_terminal'],
           data['other_c_type'],
           data['other_b_num'],
           data['other_ip_num'],
           data['complete_index'],
           data['spread_index'],
           data['law_index'],
           data['venture_index']]

    if count < 200:
        data['level_venture'] = '1'
    elif count < 10200 and count >= 200:
        data['level_venture'] = '2'
    else:
        data['level_venture'] = '3'

    if data['e_address'] in ad_address.keys():
        # data['ad_id'] = 'T' + ad_address[data['e_address']] + datetime.datetime.now().strftime('%Y%m') + data[  ######修改数据时间######
        #     'level_venture'] + getnewid(data['ad_id'])
        data['ad_id'] = 'T' + ad_address[data['e_address']] + data['ad_pushTime'][:7].replace('-','') + data['level_venture'] + getnewid(data['ad_id'])
        data['e_address'] = ad_address[data['e_address']]
    if data['m_address'] in ad_address.keys():
        data['m_address'] = ad_address[data['m_address']]

    ad_class_value = data['ad_category'].split(';')[0]

    if ad_class_value in ad_class.keys():
        data['ad_category'] = ad_class[ad_class_value]
    if data['e_category'] in e_class.keys():
        data['e_category'] = e_class[data['e_category']]

    # if count < 500000:   #####可删掉######
    writer.writerow(getlist(data))
    print(count)
    count += 1