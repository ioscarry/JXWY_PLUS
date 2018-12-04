from selenium import webdriver

opt = webdriver.ChromeOptions()
opt.add_argument('headless')
url = 'http://www.baidu.com'

# 创建浏览器配置对象
driver = webdriver.Chrome(chrome_options=opt)
driver.maximize_window()  # 设置全屏,截图也全屏, 否则默认非全屏

driver.get(url)
driver.save_screenshot('chrome_baidu.png')