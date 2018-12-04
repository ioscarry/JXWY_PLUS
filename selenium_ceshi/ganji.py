import time
from selenium import webdriver
url = 'https://bj.lianjia.com/'

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)

print(driver.window_handles)
print(driver.current_url)

js = 'scrollTo(0,500)'
driver.execute_script(js)
el_fang = driver.find_element_by_xpath('/html/body/div[2]/ul/li[1]/a/img')
time.sleep(1)
el_fang.click()
print(driver.window_handles)
print(driver.current_url)

# 通过窗口句柄切换窗口
driver.switch_to.window(driver.window_handles[-1])

node_list = driver.find_elements_by_xpath('//*[@id="leftContent"]/ul/li/div/div[1]/a')
for node in node_list:
    print(node.text,node.get_attribute('href'))