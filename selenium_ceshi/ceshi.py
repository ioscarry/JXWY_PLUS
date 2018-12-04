from selenium import webdriver
import time
def main():
    b=webdriver.Chrome()
    b.get('http://www.baidu.com')
    time.sleep(2)
    print(b.page_source)
    print(b.title)
    print(b.current_url)
    print(b.get_cookies())

    b.quit()
if __name__ == '__main__':

    main()