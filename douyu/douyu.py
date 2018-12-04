import time
from selenium import webdriver

class Spider(object):
    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()


    def parse_data(self):
        # 获取所有的房间节点列表
        room_list = self.driver.find_elements_by_xpath('//*[@id="live-new-show-content-box"]/li/a')

        data_list = []

        for room in room_list:
            temp = {}
            temp['title'] = room.find_element_by_xpath('./div/div/h3').text
            temp['type'] = room.find_element_by_xpath('./div/div/span').text
            temp['owner'] = room.find_element_by_xpath('./div/p/span[1]').text
            # temp['num'] = room.find_element_by_xpath('./div/p/span[2]').text
            # 从selenium定位到的元素中取值: get_attribute()
            temp['cover'] = room.find_element_by_xpath('./span/img').get_attribute('src')
            print(temp)
            data_list.append(temp)
        return data_list

    def save_data(self,data_list):
        pass

    def __del__(self):
        self.driver.close()

    def run(self):
        # url
        while True:
            # 发送请求
            self.driver.get(self.url)
            data_list = self.parse_data()
            self.save_data(data_list)
            # 翻页
            try:
                el_next = self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]')
                el_next.click()
                time.sleep(3)
            except:
                break

if __name__ == '__main__':
    spider = Spider()
    spider.run()