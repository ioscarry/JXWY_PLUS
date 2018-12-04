import re

import requests

url = 'http://zhibo.renren.com/top'

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',

    # 'Cookie': 'anonymid=jhrnyqaj-wdprml; depovince=BJ; _r01_=1; ick_login=136ef0cf-78bc-4120-b912-2e95a97ed630; ick=f1f352e8-3b11-4b0d-9f73-157ffe81223e; jebecookies=71aec741-fe4e-4502-aa98-4bc53165d788|||||; _de=BEF60B1E26F89514530F97F46C27D779696BF75400CE19CC; p=461a31dd5906dd5eb22769230782483d7; first_login_flag=1; ln_uact=616236330@qq.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20110810/1215/h_main_Smbo_695600031f402f75.jpg; t=bc883ba20e83b3db44387822cd0f424f7; societyguester=bc883ba20e83b3db44387822cd0f424f7; id=397428327; xnsid=4ffd45ae; loginfrom=syshome; ch_id=10016; JSESSIONID=abccRTBdeD2hkh1IRaWow'
}

cookies = 'anonymid=jhrnyqaj-wdprml; depovince=BJ; _r01_=1; ick_login=136ef0cf-78bc-4120-b912-2e95a97ed630; ick=f1f352e8-3b11-4b0d-9f73-157ffe81223e; jebecookies=71aec741-fe4e-4502-aa98-4bc53165d788|||||; _de=BEF60B1E26F89514530F97F46C27D779696BF75400CE19CC; p=461a31dd5906dd5eb22769230782483d7; first_login_flag=1; ln_uact=616236330@qq.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20110810/1215/h_main_Smbo_695600031f402f75.jpg; t=bc883ba20e83b3db44387822cd0f424f7; societyguester=bc883ba20e83b3db44387822cd0f424f7; id=397428327; xnsid=4ffd45ae; loginfrom=syshome; ch_id=10016; JSESSIONID=abccRTBdeD2hkh1IRaWow'
cookies_dict = {}
for i in cookies.split(';'):
    key = i.split('=',1)[0]
    value = i.split('=',1)[1]
    cookies_dict[key] = value

print(cookies_dict)

rsp = requests.get(url,headers=headers,cookies=cookies_dict)
with open('renren.html','wb')as f:
    f.write(rsp.content)
#
# result = re.findall('李泽华',rsp.content.decode())
#
# print(result)