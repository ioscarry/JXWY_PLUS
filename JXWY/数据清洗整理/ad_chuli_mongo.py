# -*- coding: utf-8 -*-

# 从库中取数据，公司分离出单独数据，将各个字段值处理之后存入新的集合
import mongo_config as cfg
import time
import random
from textSummary import TextSummary
import re

#  广告主信息(从mongo中比对的数据)  find/aggregate
def getADerInfo(name):
    company = cfg.dbNew
    company_d = {}
    if len(str(name)) == 0:
        company_d = {'important':"",'category': '','address': '', 'scope': '','num': ''}
    else:
        for item in company.find({'company':name,'hasGS':1}):  # 找出每条该公司的数据
            company_d = { 'important': item['important'], 'category': item['category'],
                         'address': item['address'], 'scope': item['scope'], 'num': item['num']}
    return company_d

# 媒体信息标签   sitename字段必须与mongo_config文件中的网站名一致
def getMediaInfo(name):
    dict = cfg.m_dict
    if name in dict:
        return dict[name]['m_tag']
    else:
        return '0'

# 从数据中获取正负面词库
def getLexicon(test):
    NegativeLexicon = cfg.NegativeLexicon     #[[],[],[]]
    Non_NegativeLexicon = cfg.Non_NegativeLexicon
    content = test['content']

    all_NegativeLexicon = {}
    for item in NegativeLexicon:    # 遍历总列表每一个子列表 ['','','']
        try:
            temp = {}
            temp['num'] = 0
            temp['value'] = {}
            for word in item[1:]:
                a = content.count(word)  # 计算关键词数量
                if a != 0:
                    temp['num'] += a
                    temp['value'][word] = a
            all_NegativeLexicon[item[0]] = temp      # {'num':a,'value':{'':a,'':a}}
                                                # all_NegativeLexicon = {
            #                                                              {类目:{'num':a,'value':{'':a,'':a}}},
            #                                                              {类目:{'num':a,'value':{'':a,'':a}}}
            #                                                            }
        # except AttributeError:
        #     print('content')
        #     print(test['content'])
        #     print('type')
        #     print(type(test['content']))
        except Exception as e:
            print(e)

    all_Non_NegativeLexicon = {}
    for item in Non_NegativeLexicon:
        temp = {}
        temp['num'] = 0
        temp['value'] = {}
        try:
            for word in item[1:]:
                a = content.count(word)
                if a != 0:
                    temp["num"] += a
                    temp["value"][word] = a
            all_Non_NegativeLexicon[item[0]] = temp

        except Exception as e:
            print(e)

    return all_NegativeLexicon, all_Non_NegativeLexicon

# 获取法律法规
def getLaw(test,all_NegativeLexicon):
    # all_NegativeLexicon,all_Non_NegativeLexicon = getLexicon(test)
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

# 广告摘要
def getSummary(test):
    # 处理时间
    t_time = (test['urlTime'])
    t_nian = ''
    try:
        nian = t_time.split()
        if '-' in nian[0]:
            t_nian = nian[0].split('-')
        elif '.' in nian[0]:
            t_nian = nian[0].split('.')
        if t_nian.__len__() != 3:              # 若没有发布时间，按当前时间！
            t_nian = time.strftime("%Y-%m-%d", time.localtime()).split()[0].split('-')
    except:
        t_nian = ['1970', '01', '01']

    # 处理内容
    if type(test['urlTitle']) is not str or type(test['content']) is not str:
        res = ''
    else:
        textsummary = str(TextSummary(test['urlTitle'], test['content']).CalcSummary())
        res = str(t_nian[0] + '年' + t_nian[1] + '月' + t_nian[2] + '日，' + test['md5Tag'] + '在' + test[
            'siteName'] + '发布' + textsummary)
    return res

# 根据content打标签
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
    keywordS = re.findall(pattern, str(test))
    keywords = set(keywordS)
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

# 生成完整指数
def getCompleteIndex(res):
    content_info = 100

    basic_data = 100
    if res['ad_category'] == '':
        basic_data -= 20

    company_info = 100
    if res['e_nameOfAdvertiser'] == '':
        company_info = 0
    else:
        if company_info > 0:
            if res['e_category'] == '':
                company_info -= 20
            if res['e_address'] == '':
                company_info -= 20
            if res['e_tag'] == '':
                company_info -= 20
            if res['e_Scope'] == '':
                company_info -= 20
            if res['e_num'] == '':
                company_info -= 20
    #########################
    site_info = 100
    if res['m_name'] == '':
        if site_info > 0:
            site_info -= 20
    if res['m_yu'] == '':
        if site_info > 0:
            site_info -= 20
    if res['m_icp'] == '':
        if site_info > 0:
            site_info -= 20
    if res['m_tag'] == '':
        if site_info > 0:
            site_info -= 20
    if res['m_address'] == '':
        if site_info > 0:
            site_info -= 20
    #########################
    law_info = 100
    if law_info > 0:
        if res['law_real'] == '':
            law_info -= 20
        if res['law_name'] == '':
            law_info -= 20
        if res['law_content'] == '':
            law_info -= 20
    #########################
    other_info = 50
    #########################
    final = (
            basic_data * 0.05 + content_info * 0.1 + company_info * 0.2 + site_info * 0.15 + law_info * 0.45 + other_info * 0.05)
    return final

# 生成违法指数
def getLawIndex(negKeys,res):
    SensitiveWords = negKeys
    WordsCount = len(SensitiveWords.keys())
    if WordsCount <= 0:
        CountScore = 0
    elif WordsCount > 0 and WordsCount <= 2:
        CountScore = 30
    elif WordsCount >= 3 and WordsCount <= 5:
        CountScore = 60
    else:
        CountScore = 100
    ############################
    WordsFrequency = sum(SensitiveWords.values())
    # for i in SensitiveWords.values():
    #     WordsFrequency += i
    if WordsFrequency <= 0:
        FrequencyScore = 0
    elif WordsFrequency > 0 and WordsFrequency <= 3:
        FrequencyScore = 40
    elif WordsFrequency >= 4 and WordsFrequency <= 10:
        FrequencyScore = 70
    else:
        FrequencyScore = 100
    ############################
    if '法'in res['law_name']:
        Level = 100
    else:
        Level = 70
    ############################
    StatuteCount = 0
    if res['law_real'] != '':
        StatuteCount = res['law_real'].count('|')+1
        if res['law_real'].count('业务违规')> 1:
            StatuteCount -= (res['law_real'].count('业务违规')-1)
    StatuteCount *= 20

    res = CountScore * 0.2 + FrequencyScore * 0.2 + Level * 0.3 + StatuteCount * 0.3
    return res

# 广告数据除原始字段外的其他字段都由该方法生成
def getJson(test):

    all_NegativeLexicon, all_Non_NegativeLexicon = getLexicon(test)  # num/value  关键词命中
    # 所有的词
    keys = {}
    for negkey in all_NegativeLexicon.keys():  #  子列表的各类目名
        if all_NegativeLexicon[negkey] != {}:  # 若该类目有values
            for item in all_NegativeLexicon[negkey]['value'].keys():   # 遍历每个类目中的关键词
                keys[item] = all_NegativeLexicon[negkey]['value'][item]  # 取每个关键词的词频
    # 负面次统计
    negKeys = keys     # {'key':a,'key':a}

    for key in all_Non_NegativeLexicon.keys():
        if all_Non_NegativeLexicon[key] != {}:
            for item in all_Non_NegativeLexicon[key]['value'].keys():
                keys[item] = all_Non_NegativeLexicon[key]['value'][item]

    law = getLaw(test,all_NegativeLexicon)  # 字典格式{law_real,law_name,law_content}  违反的法律内容
    company_d = getADerInfo(test['md5Tag'])  # 从公司集合匹配符合广告主体的工商信息（提前调取好工商数据并入库）
    # 最终的广告详情数据
    res = {
        'ad_id': '',
        # 采集时间
        "ad_loadTime": test['loadTime'],
        # 发表时间
        "ad_pushTime": test['urlTime'].split()[0],
        # 广告url
        "ad_url": test["urlname"],
        # 广告标题
        "ad_title": test['urlTitle'],
        # 广告所涉及的业务类型
        "ad_category": getad_category(test['content']),  # 根据content打标签
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
        'law_picid': None,

        # 其他信息
        'other_terminal': '1',
        'other_c_type': '1',
        'other_b_num': None,
        'other_ip_num': None,

        # 评价体系
        'complete_index': None,
        'spread_index': random.randrange(30,88)+random.randrange(0,100)/100,   # 传播力指数
        'law_index': None,
        'venture_index': None,
        'level_venture':None,
        'version': test['version']
    }

    res['complete_index'] = getCompleteIndex(res)
    res['law_index']=getLawIndex(negKeys,res)
    res['venture_index'] = 0.5 * res['law_index'] + 0.3 * res['complete_index']+0.2 * res['spread_index']
    if res['venture_index'] > 71.6:
        res['level_venture'] = 'Ⅰ类'
    elif res['venture_index']<=71.6 and res['venture_index']>=69:
        res['level_venture'] = 'Ⅱ类'
    elif res['venture_index'] < 69:
        res['level_venture'] = 'Ⅲ类'
    else:
        res['venture_index'] = ''

    return res

# 对content做一下处理，去掉干扰字符和换行问题，替换（第一遍处理）
def ContentTreat(item):
    item = re.sub('<[\s\S]*?>','',str(item)).strip().replace('\r\n', '@@@rn@@@').replace(u'\001', '@@@001@@@')
    return item

if __name__ == '__main__':

    source_col = cfg.dbOld.copy   # 需要处理的原数据库
    final_col = cfg.dbOld.final_adv_all   # 处理后存放的数据库
    version = '20181231'
    index = 1
    for item in source_col.find():   # 每条数据预处理
        if item['content'].strip() > 0:   # 筛选出content非空数据
            ad_d = {       # 数据的第一遍清洗
                    'urlTitle': item['urltitle'].strip(),
                    'urlTime': item['urltime'].strip(),
                    'md5Tag': str(item['company']).strip(),   # 报错 AttributeError: 'int' object has no attribute 'strip'
                    'content': ContentTreat(item['content'].strip()),
                    'siteName': item['sitename'].strip(),
                    'yuming': item['yuming'].strip(),
                    'icp': item['icp'].strip(),
                    'icpsheng': item['icpsheng'].strip(),
                    'loadTime': item['updatetime'].strip(),
                    'urlname': item['urlname'].strip(),
                    'ABSTRACT': "",
                    'class': item['category'],
                    'version': version
                    }
            res = getJson(ad_d)        # 对数据详细处理

            if res['ad_KeyWords'] != {}:
                res['ad_id'] = index
                final_col.insert_one(res)
                index += 1
                # print(res)