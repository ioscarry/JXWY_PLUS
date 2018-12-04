import time
from selenium import webdriver

url = 'http://www.baidu.com'

driver = webdriver.Chrome()
driver.get(url)

# 定位到搜索框
el_input = driver.find_element_by_id("kw")

el_input.send_keys('你奶奶的')
el_sub = driver.find_element_by_css_selector('#su')
el_sub.click()
print(driver.window_handles)
time.sleep(3)
# el_text = driver.find_element_by_xpath('//*[@id="1"]/h3/a')
el_text = driver.find_element_by_xpath('//*[@id="10"]/h3/a')
time.sleep(3)
el_text.click()