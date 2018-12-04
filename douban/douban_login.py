from selenium import webdriver
import requests
from douban.yundama import identify
url = 'https://accounts.douban.com/login'
driver = webdriver.Chrome()
driver.get(url)

# 定位账号框, 输入
el_user = driver.find_element_by_id('email')
el_user.send_keys('m17173805860@163.com')

# 定位密码输入框，并输入
el_pwd = driver.find_element_by_id('password')
el_pwd.send_keys('1qaz@WSX3edc')

# 点击登陆
el_sub = driver.find_element_by_name('login')
el_sub.click()

# 定位验证码图片，下载并打码
try:
    el_img = driver.find_element_by_id('captcha_image')
except:
    data = driver.page_source
    print(data)
else:
    url = el_img.get_attribute('src')
    data = requests.get(url).content
    result = identify(data)

    # 输入验证码
    el_captcha = driver.find_element_by_id('captcha_field')
    el_captcha.send_keys(result)

    # 点击登陆
    el_sub = driver.find_element_by_name('login')
    el_sub.click()