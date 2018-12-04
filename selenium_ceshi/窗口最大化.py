from selenium import webdriver


driver = webdriver.Chrome()

driver.maximize_window()

driver.close()

# 查看方法
print(dir(driver))