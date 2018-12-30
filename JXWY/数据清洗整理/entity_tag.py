import pandas as pd
import csv
"""
根据公司名判断类别，使用关键字匹配，同时要注意是不是在网贷名单表内，如果在就是p2p类型
"""
# 判断是否在网贷名单里，如果在tag为true,并且保存在新表里
# p2p = pd.read_csv(r"C:\Users\zhd\Desktop\广告数据处理\p2p_csv.csv",encoding='',engine='python')
# ad = pd.read_csv(r"C:\Users\zhd\Desktop\广告数据处理\9000照面.csv",encoding="",engine='python')
# df = pd.merge(ad,p2p,how="left",on="company")
# df.to_csv("ad2.csv")
#
df = pd.read_csv("ad2.csv",encoding="utf-8")
tag = df["tag"]
entity_name = df["company"]

with open("entity_tag.csv", "a",newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for i in range(0,len(df)):
        # print(tag[i])
        if tag[i] == 'TRUE':
            result = "p2p网贷"
        else:
            if type(entity_name[i]) != str:
               result = " "
            else:
                if '支付' in entity_name[i]:
                    result = "支付机构"
                elif '信用评估'in entity_name[i] or '征信' in  entity_name[i] or '信用管理' in entity_name[i]:
                    result = "征信机构"
                elif '外汇' in entity_name[i]:
                    result = "外汇机构"
                elif '银行' in entity_name[i]:
                    result = "银行机构"
                elif '证券' in entity_name[i] or '股权' in  entity_name[i] or '基金' in entity_name[i] or  '有限合伙' in entity_name[i] or '信托' in entity_name[i]:
                    result = "证券机构"
                elif '期货' in entity_name[i]:
                    result = "期货机构"
                elif '保险' in entity_name[i]:
                    result = "保险机构"
                elif '小额贷款' in entity_name[i] or '小贷' in entity_name[i]:
                    result = "地方小额贷款机构"
                elif '贷款' in entity_name[i]:
                    result = "网络贷款机构"
                elif '融资担保' in entity_name[i]:
                    result = "融资担保机构"
                elif '典当' in entity_name[i]:
                    result = "典当机构"
                elif '保理' in entity_name[i]:
                    result = "商业保理机构"
                elif '金融信息服务' in entity_name[i] or '金融服务' in entity_name[i] or '财富管理' in entity_name[i] or '投资' in entity_name[i] or '理财顾问' in entity_name[i] or '资产管理' in entity_name[i] or '资本管理' in entity_name[i] or '理财咨询' in entity_name[i]or '理财服务' in entity_name[i] or '投融资' in entity_name[i] or '财富信息' in entity_name[i] or '创投管理顾问'in entity_name[i]:
                    result = "民间借贷相关机构"
                elif entity_name[i] == []:
                    result = " "
                else:
                    result = "其他（非持牌机构）"
        writer.writerow([result])





