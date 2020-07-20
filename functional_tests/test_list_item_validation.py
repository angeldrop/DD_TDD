from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip


            
class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #伊迪丝访问首页，不小心提交了一个空待办事项
        #输入框中没输入内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        #首页刷新了，显示一个错误消息
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '你不能输入空项目'
        ))
        #提示待办事项不能为空#她输入一些文字，然后再次提交，这次没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('买牛奶')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:买牛奶')

        #她有点儿调皮，又提交了一个空待办事项
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        #在清单页面她看到了一个类似的错误消息
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '你不能输入空项目'
        ))

        #输入文字之后就没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('弄杯茶')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2:弄杯茶')
        self.fail('非法值测试完了')


     