from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class LayoutAndStyingTest(FunctionalTest):
    def test_layout_and_styling(self):
        #伊迪丝听说有一个很酷的在线待办事项应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        
        #她注意到输入框完美的居中显示
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
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
            
          