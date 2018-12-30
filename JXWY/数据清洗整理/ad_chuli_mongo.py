# -*- coding: utf-8 -*-

# 从库中取数据，公司表分离出单独数据
import mongo_config as cfg
import time
import random
from textSummary import TextSummary
import re

#  广告主信息(从mongo中比对的数据)
def getADerInfo(name):
    company = cfg.dbNew
    company_d = {'important':"",'category': '','address': '', 'scope': '','num': ''}
    if len(str(name)) == 0:
        company_d = {'important':"",'category': '','address': '', 'scope': '','num': ''}
    else:
        for item in company.find({'company':name,'hasGS':"1"}):
            company_d = { 'important': item['important'], 'category': item['category'],
                         'address': item['address'], 'scope': item['scope'], 'num': item['num']}
    return company_d

# 媒体信息标签
def getMediaInfo(name):
    dict = cfg.m_dict
    if name in dict:
        return dict[name]['m_tag']
    else:
        return '0'

# 获取正负面词库
def getLexicon(test):
    NegativeLexicon = cfg.NegativeLexicon
    Non_NegativeLexicon = cfg.Non_NegativeLexicon
    all_NegativeLexicon = {}
    for item in NegativeLexicon:
        # print(item)
        try:
            temp = {}
            for word in item[1:]:
                content = ''
                if test['content'] != {}:
                    content = test['content']
                a = content.count(word)
                if a is not 0:
                    # print(word, a)
                    if 'num' not in temp.keys():
                        temp['num'] = a
                    else:
                        temp['num'] += a

                    if "value" not in temp.keys():
                        temp['value'] = {}
                        temp['value'][word] = a
                    # print(temp)
            all_NegativeLexicon[item[0]] = temp
        except AttributeError:
            print('content')
            print(test['content'])
            print('type')
            print(type(test['content']))
    all_Non_NegativeLexicon = {}
    for item in Non_NegativeLexicon:
        temp = {}
        try:
            for word in item[1:]:
                content = ''
                if test['content'] != {}:
                    content = test['content']
                a = content.count(word)
                if a is not 0:
                    # print(word, a)
                    if 'num' not in temp.keys():
                        temp["num"] = a
                    else:
                        temp["num"] += a

                    if "value" not in temp.keys():
                        temp["value"] = {}
                        temp["value"][word] = a
            all_Non_NegativeLexicon[item[0]] = temp
        except AttributeError:
            print('content')
            print(test['content'])
            print('type')
            print(type(test['content']))
    return all_NegativeLexicon, all_Non_NegativeLexicon

# 获取法律法规
def getLaw(test):
    all_NegativeLexicon, all_Non_NegativeLexicon = getLexicon(test)
    c1 = []
    c2 = []
    c3 = []

    #业务违规
    if all_NegativeLexicon["其它负面"] != {}:
        law_real = "业务违规"
        law_name = "《关于处置非法集资活动中加强广告审查和监管工作有关问题的通知》"
        law_content = "《关于处置非法集资活动中加强广告审查和监管工作有关问题的通知》第二条第三、四款"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)
    if all_NegativeLexicon["虚假/夸大宣传"] != {} and ('贷款' in test['class']) :
        law_real = "业务违规"
        law_name = "《网络借贷信息中介机构业务活动管理暂行办法》"
        law_content = "《网络借贷信息中介机构业务活动管理暂行办法》第十条第十款"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)
    if all_NegativeLexicon["传销"] != {} or all_NegativeLexicon["消费返利（电子商务）"] != {}:
        law_real = "业务违规"
        law_name = "《消费者权益保护法》;《中华人民共和国广告法》;《反不正当竞争法》"
        law_content = "消费者权益保护法》第二十条;《中华人民共和国广告法》第二十八条，第九条第三款，第四条;《反不正当竞争法》第八条，第九条，第十一条"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)
    # 提供增信  虚假/夸大宣传
    if all_NegativeLexicon["虚假/夸大宣传"] != {}:
        if all_NegativeLexicon["提供增信"] != {}:
            if ('贷款' in test['class']):
                law_real = "提供增信"
                law_name = "《互联网金融风险专项整治工作实施方案》"
                law_content = "《互联网金融风险专项整治工作实施方案》第二条第一款"
            else:
                law_real = "提供增信"
                law_name = "《开展互联网金融广告及以投资理财名义从事金融活动风险专项整治工作实施方案》"
                law_content = "《开展互联网金融广告及以投资理财名义从事金融活动风险专项整治工作实施方案》第二条第四款"
        else:
            law_real = "虚假/夸大宣传"
            law_name = "《消费者权益保护法》;《中华人民共和国广告法》;《反不正当竞争法》;《互联网广告管理暂行办法》;《互联网金融从业机构营销和宣传活动自律公约 (试行 ) 》;《互联网金融风险专项整治工作实施方案》"
            law_content = "消费者权益保护法》第二十条;《中华人民共和国广告法》第二十八条，第九条第三款，第四条;《反不正当竞争法》第八条，第九条，第十一条;互联网广告管理暂行办法》第十六条;《互联网金融从业机构营销和宣传活动自律公约 (试行 ) 》第十四条,第十八条,第二十五条;《互联网金融风险专项整治工作实施方案》第二条第四款"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)

    # 贷款审核
    if all_NegativeLexicon["贷款审核"] != {}:
        law_real = "放款审核"
        law_name = "《网络借贷信息中介机构业务活动管理暂行办法》"
        law_content = "《网络借贷信息中介机构业务活动管理暂行办法》第二十一条，第九条第二款，第十七条"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)


    # 提供增信
    if all_NegativeLexicon["提供增信"] != {}:
        if ('贷款' in test['class']):
            law_real = "提供增信"
            law_name = "《关于促进互联网金融健康发展的指导意见》;《网络借贷信息中介机构业务活动管理暂行办法》"
            law_content = "《关于促进互联网金融健康发展的指导意见》第二条第八款;网络借贷信息中介机构业务活动管理暂行办法》第三条第一款,第十条第三款"

        else:
            law_real = "提供增信"
            law_name = "《中华人民共和国广告法》"
            law_content = "《中华人民共和国广告法》第二十五条第一款"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)


    #高息利诱
    if all_NegativeLexicon["高息利诱"] != {}:
        law_real = "高息利诱"
        law_name = "《互联网金融风险专项整治工作实施方案》"
        law_content = "《互联网金融风险专项整治工作实施方案》第三条第四款"
        c1.append(law_real)
        c2.append(law_name)
        c3.append(law_content)

    law_real = '|'.join(c1)
    law_name = '|'.join(c2)
    law_content = '|'.join(c3)
    # print(law_real,c1,c2,c3)
    return {"law_real": law_real, "law_name": law_name, "law_content": law_content}

def getSummary(test):
    t_time = (test['urlTime'])
    try:
        nian = t_time.split()
        if '-' in nian[0]:
            t_nian = nian[0].split('-')
        elif '.' in nian[0]:
            t_nian = nian[0].split('.')
        if t_nian.__len__() != 3:
            a = time.strftime("%Y-%m-%d", time.localtime()).split()[0]
            a = a.split('-')
            t_nian = a
    except:
        t_nian = ['1970', '01', '01']


    if type(test['urlTitle']) is not str or type(test['content']) is not str:
        ABSTRACT = ''
    else:
        textsummary = TextSummary()
        textsummary.SetText(test['urlTitle'], test['content'])
        ABSTRACT = str(textsummary.CalcSummary())
        



    if ABSTRACT == '':
        res = ''
    else:
        res = str(t_nian[0] + '年' + t_nian[1] + '月' + t_nian[2] + '日，' + test['md5Tag'] + '在' + test[
            'siteName'] + '发布' + ABSTRACT)
    return res

def getad_category(test):
    pattern = re.compile(u"人民币收藏|错版钞|连体钞|"
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
    keywords = re.findall(pattern, str(test['content']))
    keywords = set(keywords)

    result = []
    if len(keywords) == 0:
        ad_category = '其他'
        result.append(ad_category)

    else:
        if '人民币收藏' in keywords or '错版钞' in keywords or '连体钞' in keywords:
            ad_category = '人民币业务'
            result.append(ad_category)

        if '纪念钞' in keywords or '纪念币' in keywords or '金银币' in keywords or '邮币卡' in keywords or '炒邮票' in keywords:
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
                or '极速贷' in keywords or '车贷' in keywords or '抵押贷' in keywords or '下款' in keywords or '放款' in keywords \
                or '房贷' in keywords or '微粒贷' in keywords or '芝麻分贷' in keywords or '企业贷' in keywords or '信贷' in keywords:
            ad_category = '贷款业务'
            result.append(ad_category)

        if '优选理财' in keywords or '资产管理' in keywords or '投资理财' in keywords or '理财规划' in keywords \
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
                or '掉期' in keywords or '期权合约' in keywords or '期货合约' in keywords:
            ad_category = '金融衍生品业务'
            result.append(ad_category)

        if 'P2P' in keywords or '网贷' in keywords or '网络借贷' in keywords or '借贷平台' in keywords:
            ad_category = '个体网络借贷（P2P)'
            result.append(ad_category)

    return ';'.join(result)

def getJson(test):
    all_NegativeLexicon, all_Non_NegativeLexicon = getLexicon(test)
    # 所有的词
    keys = {}
    # 负面次统计
    negKeys={}
    for key in all_NegativeLexicon.keys():
        if all_NegativeLexicon[key] != {}:
            for item in all_NegativeLexicon[key]['value'].keys():
                keys[item] = all_NegativeLexicon[key]['value'][item]
    negKeys = keys
    for key in all_Non_NegativeLexicon.keys():
        if all_Non_NegativeLexicon[key] != {}:
            for item in all_Non_NegativeLexicon[key]['value'].keys():
                keys[item] = all_Non_NegativeLexicon[key]['value'][item]


    law = getLaw(test)
    company_d = getADerInfo(test['md5Tag'])
    # 最终的广告详情数据
    import json
    res = {
        # "NegativeLexicon": all_NegativeLexicon,
        # "Non_NegativeLexicon": all_Non_NegativeLexicon,
        'ad_id': None,
        # 采集时间
        "ad_loadTime": test['loadTime'],
        # 发表时间
        "ad_pushTime": test['urlTime'].split()[0],
        # 广告url
        "ad_url": test["urlname"],
        # 广告标题
        "ad_title": test['urlTitle'],
        # 广告所涉及的业务类型
        "ad_category": getad_category(test),
        # 关键词
        "ad_KeyWords": str(keys).replace("'", '"'),
        # 关键词个数
        "ad_numOfKeyWords": keys.__len__(),
        # 关键词词频
        "ad_frequencyOfKeyWords": sum(keys.values()),
        # 新闻字数
        'ad_numOfContent': test['content'].__len__(),
        # 广告摘要
        'ad_summary': getSummary(test),
        # 广告正文
        'ad_content': test['content'],

        # 广告主名称
        'e_nameOfAdvertiser': test['md5Tag'],
        # 广告主行业类型
        'e_category': company_d['category'],
        'e_address': company_d['address'],
        'e_tag': company_d['important'],
        'e_Scope': company_d['scope'],
        'e_num': company_d['num'],

        # 媒体相关数据
        'm_name': test['siteName'],
        'm_yu': test['yuming'],
        'm_icp': test['icp'],
        'm_tag': getMediaInfo(test['siteName']),
        'm_address': test['icpsheng'],

        # 法律相关数据
        'law_real': law['law_real'],
        'law_name': law['law_name'],
        'law_content': law['law_content'],
        'law_picid': '',

        # 其他信息
        'other_terminal': '1',
        'other_c_type': '1',
        'other_b_num': None,
        'other_ip_num': None,

        # 评价体系
        'complete_index': None,
        'spread_index': random.randrange(30,88)+random.randrange(0,100)/100,
        'law_index': None,
        'venture_index': None,
        'level_venture':None,
        'version': test['version']
    }

    def getCompleteIndex(res):
        jichuxinxi = 100
        if res['ad_category'] is None:
            jichuxinxi -= 20

        zhengwenneirong = 100
        guanggaozhuxinxi = 100
        if res['e_nameOfAdvertiser'] is None or len(res['e_nameOfAdvertiser']) == 0 :
            guanggaozhuxinxi = 0
        elif res['e_nameOfAdvertiser'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        if res['e_category'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        if res['e_address'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        if res['e_tag'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        if res['e_Scope'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        if res['e_num'] is None:
            if guanggaozhuxinxi > 0:
                guanggaozhuxinxi -= 20
        #########################
        guanggaomeijiexinxi = 100
        if res['m_name'] is not None:
            if guanggaomeijiexinxi > 0:
                guanggaomeijiexinxi -= 20
        if res['m_yu'] is None:
            if guanggaomeijiexinxi > 0:
                guanggaomeijiexinxi -= 20
        if res['m_icp'] is None:
            if guanggaomeijiexinxi > 0:
                guanggaomeijiexinxi -= 20
        if res['m_tag'] is None:
            if guanggaomeijiexinxi > 0:
                guanggaomeijiexinxi -= 20
        if res['m_address'] is None:
            if guanggaomeijiexinxi > 0:
                guanggaomeijiexinxi -= 20
        #########################
        weifaweiguixinxi = 100
        # 'law_picid':
        if res['law_real'] is None:
            if weifaweiguixinxi > 0:
                weifaweiguixinxi -= 20
        if res['law_name'] is None:
            if weifaweiguixinxi > 0:
                weifaweiguixinxi -= 20
        if res['law_content'] is None:
            if weifaweiguixinxi > 0:
                weifaweiguixinxi -= 20
        #########################
        qitaxinxi = 50
        #########################
        xinxiwanzhengxing = (
                    jichuxinxi * 0.05 + zhengwenneirong * 0.1 + guanggaozhuxinxi * 0.2 + guanggaomeijiexinxi * 0.15 + weifaweiguixinxi * 0.45 + qitaxinxi * 0.05)
        return xinxiwanzhengxing

    res['complete_index'] = getCompleteIndex(res)

    def getLawIndex(res):
        ############################
        minganci=negKeys
        ############################
        shuliang=len(minganci.keys())
        if shuliang<=0:
            shuliang=0
        elif shuliang>0 and shuliang<=2:
            shuliang=30
        elif shuliang>=3 and shuliang<=5:
            shuliang=60
        else:
            shuliang=100
        ############################
        cipin=0
        for i in minganci.values():
            cipin+=i
        if cipin<=0:
            cipin=0
        elif cipin>0and cipin<=3:
            cipin=40
        elif cipin>=4 and cipin<=10:
            cipin=70
        else:
            cipin=100
        ############################
        dengji=0
        if '法'in res['law_name']:
            dengji=100
        else:
            dengji=70
        ############################
        tiaolishuliang=0
        if res['law_real']is not '':
            tiaolishuliang=res['law_real'].count('|')+1
            if res['law_real'].count('业务违规')>1:
                tiaolishuliang -= (res['law_real'].count('业务违规')-1)
        tiaolishuliang*=20

        res=shuliang*0.2+cipin*0.2+dengji*0.3+tiaolishuliang*0.3
        return res

    res['law_index']=getLawIndex(res)
    res['venture_index'] = 0.5*res['law_index'] + 0.3*res['complete_index']+0.2*res['spread_index']
    if res['venture_index'] > 71.6:
        res['level_venture'] = 'Ⅰ类'
    elif res['venture_index']<=71.6 and res['venture_index']>=69:
        res['level_venture'] = 'Ⅱ类'
    elif res['venture_index'] < 69:
        res['level_venture'] = 'Ⅲ类'
    else:res['venture_index'] = ''

    return res

# 对content做一下处理，去掉干扰字符和换行问题
def queren(item):
    item = re.sub('<[\s\S]*?>','',str(item)).strip().replace('\r\n', '@@@rn@@@').replace(u'\001', '@@@001@@@')
    return item

if __name__ == '__main__':

    # 连接所需数据库,test为数据库名
    source_col = cfg.dbOld.copy
    final_col = cfg.dbOld.final_adv_all
    version = '20181231'
    # 取数据标记，获取原始数据
    # out_dict = {'out_version': '20181201'}
    # for i in final_col.find({}).sort('_id', pymongo.DESCENDING).limit(1):
    #     index = i['ad_id']
    index = 1
    for item in source_col.find():
        ad_d = {'urlTitle': item['urltitle'].strip(),
                'urlTime': item['urltime'].strip(),
                'md5Tag': str(item['company']).strip(),   # 报错 AttributeError: 'int' object has no attribute 'strip'
                'content': queren(item['content'].strip()),
                'siteName': item['sitename'].strip(),
                'yuming': item['yuming'].strip(),
                'icp': item['icp'].strip(),
                'icpsheng': item['icpsheng'].strip(),
                'loadTime': item['updatetime'].strip(),
                'urlname': item['urlname'].strip(),
                'ABSTRACT': "",
                'class': item['category'],
                'version': version}
        if len(ad_d['content']) > 0:
            res = getJson(ad_d)
            if res['ad_KeyWords'] != '{}':
                res['ad_id'] = index
                # inert
                final_col.insert_one(res)
                index += 1
                # print(res)






