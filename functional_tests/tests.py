from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #伊迪丝听说有一个很酷的在线待办事项应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #她注意到网页的标题和头部都包含“待办事项”这个词
        self.assertIn('待办事项系统' ,self.browser.title)
        head_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('你的清单' ,head_text)
        
        #应用邀请她输入一个待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '请输入待办事项'
        )

        #她在一个文本框中输入了“购买孔雀羽毛”
        #伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('购买孔雀羽毛')

        #她按回车键后，页面更新了
        #待办事项表格中显示了“1、购买孔雀羽毛”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1:购买孔雀羽毛')
        
        #页面中又显示了一个文本框，可以输入其他的待办事项
        #她输入了“使用孔雀羽毛做假蝇”
        #伊迪丝做事很有条理
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀羽毛做假蝇')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        #页面再次更新，她的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1:购买孔雀羽毛')
        self.check_for_row_in_list_table('2:使用孔雀羽毛做假蝇')
        
        #伊迪丝想知道这个网站是否会记住她的清单
        #她看到网站为她生成了一个唯一的URL
        #而且页面中有一些文字解说这个功能
        self.fail('结束测试')
        #她访问那个URL，发现她的待办事项列表还在

        #她很满意，去睡觉了
        
 