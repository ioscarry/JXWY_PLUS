from selenium import webdriver
import time

opt = webdriver.ChromeOptions()
opt.add_argument('headless')
driver = webdriver.Chrome(chrome_options=opt)
driver.get('http://www.baidu.com')
time.sleep(2)
# driver.save_screenshot('hehe.jpg')
cookies= driver.get_cookies()
print(cookies)
driver.close()
for cookie in cookies:
    print('%s -> %s'%(cookie['name'],cookie['value']))