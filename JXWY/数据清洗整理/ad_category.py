import pandas as pd
import re
import csv

"""
根据广告内容进行关键词匹配来判断广告类别，可能会出现多个类别，使用分号隔开。
"""
excel = pd.read_csv("data/ad.csv",encoding="utf-8")
ad_content = excel["content"]
pattern =re.compile(u"人民币收藏|错版钞|连体钞|"
                    u"纪念钞|纪念币|金银币|邮币卡|炒邮票|"
                    u"免费安装POS机|第三方支付|免费送POS机|POS机代理加盟|"
                    u"征信服务|征信业务|信用评估|"
                    u"外汇|"
                    u"贵金属|黄金|原油|白银|石油|"
                    u"放贷|配资|信用贷|无抵押贷款|小额贷款|极速贷|车贷|抵押贷|下款|放款|房贷|微粒贷|芝麻分贷|企业贷|信贷|"
                    u"优选理财|资产管理|投资理财|理财规划|P2P|网贷|网络借贷|借贷平台|"
                    u"证券|券商|信托|私募|公募|"
                    u"众筹|"
                    u"保险经纪|寿险|财产险|养老险|意外险|健康险|商业保险|汽车保险|"
                    u"期货|期权|双向交易|T\+0|"
                    u"金融合约|金融衍生品|标准化合约|远期合约|掉期|期权合约|期货合约|"
                    u"P2P|网贷|网络借贷|借贷平台")
with open("data/ad_category.csv", "a",newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for i in range(0,len(excel)):
        keywords = re.findall(pattern, str(ad_content[i]))
        keywords = list(set(keywords))
        result = []
        if keywords == []:
            ad_category = '其他'
            result.append(ad_category)

        if '人民币收藏' in keywords or '错版钞' in keywords or '连体钞' in keywords:
            ad_category = '人民币业务'
            result.append(ad_category)

        if  '纪念钞' in keywords or '纪念币'in keywords or '金银币' in keywords or '邮币卡' in keywords or '炒邮票' in keywords:
            ad_category = '纪念币业务'
            result.append(ad_category)

        if '免费安装POS机' in keywords or '第三方支付' in keywords or '免费送POS机' in keywords or 'POS机代理加盟' in keywords:
            ad_category = '支付结算业务'
            result.append(ad_category)

        if '征信服务' in keywords or '征信业务' in keywords or '信用评估' in keywords:
            ad_category = '征信业务'
            result.append(ad_category)

        if '外汇' in keywords:
            ad_category = '外汇业务'
            result.append(ad_category)

        if '贵金属' in keywords or '黄金' in keywords or '原油' in keywords or '白银' in keywords or '石油' in keywords:
            ad_category = '贵金属业务'
            result.append(ad_category)

        if '放贷' in keywords or '配资' in keywords or '信用贷' in keywords or '无抵押贷款' in keywords or '小额贷款' in keywords \
                or '极速贷'in keywords or '车贷'in keywords or '抵押贷'in keywords or '下款'in keywords or '放款'in keywords\
                or '房贷' in keywords or '微粒贷' in keywords or '芝麻分贷' in keywords or '企业贷'in keywords or '信贷'  in keywords:
            ad_category = '贷款业务'
            result.append(ad_category)

        if '优选理财'in keywords or '资产管理' in keywords or '投资理财' in keywords or '理财规划' in keywords \
                or 'P2P' in keywords or '网贷' in keywords or '网络借贷' in keywords or '借贷平台' in keywords:
            ad_category = '投资理财业务'
            result.append(ad_category)

        if '证券' in keywords or '券商' in keywords or '信托' in keywords or '私募' in keywords or '公募' in keywords:
            ad_category = '证券业务'
            result.append(ad_category)

        if '众筹' in keywords:
            ad_category = '众筹业务'
            result.append(ad_category)

        if '保险经纪' in keywords or '寿险' in keywords or '财产险' in keywords or '养老险' in keywords \
                or '意外险' in keywords or '健康险' in keywords or '商业保险' in keywords or '汽车保险' in keywords:
            ad_category = '保险业务'
            result.append(ad_category)

        if '期货' in keywords or '期权' in keywords or '双向交易' in keywords or 'T+0' in keywords:
            ad_category = '期货业务'
            result.append(ad_category)

        if '金融合约' in keywords or '金融衍生品' in keywords or '标准化合约' in keywords or '远期合约' in keywords \
                or '掉期' in keywords or '期权合约' in keywords or '期货合约'  in keywords:
            ad_category = '金融衍生品业务'
            result.append(ad_category)

        if 'P2P' in keywords or '网贷'in keywords or '网络借贷'in keywords or '借贷平台' in keywords:
            ad_category = '个体网络借贷（P2P)'
            result.append(ad_category)


        writer.writerow([';'.join(result)])