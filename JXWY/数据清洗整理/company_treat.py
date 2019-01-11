

def getE_category(test):

    if test in cfg.e_p2p:
        print(cfg.e_p2p[test])
    else:
        if '支付' in test:
            result = "支付机构"
        elif '信用评估' in test or '征信' in test or '信用管理' in test:
            result = "征信机构"
        elif '外汇' in test:
            result = "外汇机构"
        elif '银行' in test:
            result = "银行机构"
        elif '证券' in test or '股权' in test or '基金' in test or '有限合伙' in test or '信托' in test:
            result = "证券机构"
        elif '期货' in test:
            result = "期货机构"
        elif '保险' in test:
            result = "保险机构"
        elif '小额贷款' in test or '小贷' in test:
            result = "地方小额贷款机构"
        elif '贷款' in test:
            result = "网络贷款机构"
        elif '融资担保' in test:
            result = "融资担保机构"
        elif '典当' in test:
            result = "典当机构"
        elif '保理' in test:
            result = "商业保理机构"
        elif '金融信息服务' in test or '金融服务' in test or '财富管理' in test or '投资' in test or '理财顾问' in test or '资产管理' in test or '资本管理' in test or '理财咨询' in \
                test or '理财服务' in test or '投融资' in test or '财富信息' in test or '创投管理顾问' in test:
            result = "民间借贷相关机构"
        elif len(test) == 0:
            result = ""
        else:
            result = "其他（非持牌机构）"
        print(result)
        pass



def getE_address(num):
    test = {}
    test['num'] = num
    area = cf.area_id
    a = str(test['num']).strip()[:4]
    if a in area:
        return area[a]
    else:
        return ''