from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest


MAX_WAIT=10
class NewVisitorTest(LiveServerTestCase):


    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_and_retrieve_it_later(self):
        #伊迪丝听说有一个很酷的在线待办事项应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #她注意到网页的标题和头部都包含“待办事项”这个词
        self.assertIn('待办事项系统' ,self.browser.title)
        head_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('你的清单' ,head_text)
        
        #她注意到输入框完美的居中显示
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
            )
        
        

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
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')
        #输入框依然完美的居中显示
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
            )

        #页面中又显示了一个文本框，可以输入其他的待办事项
        #她输入了“使用孔雀羽毛做假蝇”
        #伊迪丝做事很有条理
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀羽毛做假蝇')
        inputbox.send_keys(Keys.ENTER)


        #页面再次更新，她的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')
        self.wait_for_row_in_list_table('2:使用孔雀羽毛做假蝇')
        
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('购买孔雀羽毛')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')

        #伊迪丝想知道这个网站是否会记住她的清单
        #她看到网站为她生成了一个唯一的URL
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        
        #现在一名叫作弗朗西斯的新用户访问了网站
        
        ##我们使用一个新浏览器会话
        ##确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser=webdriver.Firefox()
        
        #弗朗西斯访问首页
        #页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀羽毛',page_text)
        self.assertNotIn('使用孔雀羽毛做假蝇',page_text)
        
        #弗朗西斯输入一个新待办事项，新建一个清单
        #他不像伊迪丝那样兴趣盎然
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('买牛奶')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:买牛奶')
        
        #弗朗西斯获得了他的唯一URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
        
        #这个页面还是没有伊迪丝的清单
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀羽毛',page_text)
        self.assertNotIn('使用孔雀羽毛做假蝇',page_text)
        
        #两人都很满意，然后去睡觉了
        #而且页面中有一些文字解说这个功能
        self.fail('结束测试')
        #她访问那个URL，发现她的待办事项列表还在

        #她很满意，去睡觉了

 