import time
from selenium import webdriver

url = 'https://qzone.qq.com/'

driver = webdriver.Chrome()
driver.get(url)

# 切换到iframe框架登录
el_frame = driver.find_element_by_xpath('//*[@id="login_frame"]')
driver.switch_to.frame(el_frame)
# 点击使用账号密码登录
el_up = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
el_up.click()
time.sleep(2)

el_user = driver.find_element_by_xpath('//*[@id="u"]')
el_user.send_keys('616236330')
el_pwd = driver.find_element_by_id('p')
el_pwd.send_keys('HIU.maksim')
el_sub = driver.find_element_by_id('login_button')
el_sub.click()