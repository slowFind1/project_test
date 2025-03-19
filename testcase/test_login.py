from time import sleep

import allure
import pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By
from common.selenium_common import sel_click,element_visible,element_clickable,send_keys,get_text
from po.event import Event
from settings import Environment

class TestLogin:

    # def setup_class(self):              # 类方法，在类开始时执行，只执行一次,只需要打开一次浏览器，然后运行下面的测试
    #     print("开始测试")
    #     self.driver = webdriver.Chrome()
    #     self.driver.get("http://127.0.0.1:8000/")
    #     self.driver.maximize_window()
    #     self.driver.implicitly_wait(10)
    #
    # def teardown_class(self):          # 类方法，在类结束时执行，只执行一次; 在下面所有测试用例执行完毕，才会执行此函数
    #     print("结束测试")
    #     self.driver.quit()



    '''
        对于前3个用例来说，几个步骤都一眼，用户登录，输入密码 ；
        我们通过下面方法进行优化;编辑一个列表，存放三个测试用例所需要的用户名字，密码，以及结果;
        那么我们可以通过一个测试用例，替换三个用例编写代码； 002，003将不在需要
    '''
    @pytest.mark.parametrize('username,password,result',[
        (Environment.username,Environment.password,"欢迎您：test1234567 | 退出"),
        ("bucunzai",Environment.password,'用户名错误'),
        (Environment.username,"mimacuowu",'密码错误'),
    ],ids=(
            'test_shopping_mall_001',
            'test_shopping_mall_002',
            'test_shopping_mall_003',

            #设置上述测试名称001- 003 的测试用例名称
    ))
    @allure.feature("登录测试")
    @allure.story("登录")
    def test_shopping_mall(self,username,password,result,open_homepage):   # 测试用例1：正常登录测试，用户密码正确

        #——————————打开浏览器，最大化页面，然后隐式等待——————————
        # driver = webdriver.Chrome()           #实例化，打开了chrome浏览器，通过驱动
        # driver.get("http://127.0.0.1:8000/")  #打开一个浏览器地址; 打开网页
        # driver.maximize_window()              #窗口最大化
        # driver.implicitly_wait(10)            #隐式等待


        ''''''
        '''
        
        #写法二：
        driver = open_page
        driver.get(Environment.url)             #访问首页
        
        '''


        '''  写法登录1：用写法2优化替代
        driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()          #根据xpath位置，然后点击登录按钮

        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys("test123456") #输入用户名
        driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(username)

        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys("759667506")   #输入密码
        driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(password)

        driver.find_element(By.XPATH,"//input[@value='登录']").click()                            #点击登录按钮
        '''


        # 写法登录2：已经优化；用po库中Even.event_login 替换； 且已经集成在confest中 login模块
        # 但是测试三条用例，那么又不能一次性替换
        '''
        sel_click(driver, (By.XPATH,"//a[contains(text(),'登录')]"))
        send_keys(driver, (By.XPATH,"//input[@placeholder='请输入用户名']"),username)
        send_keys(driver, (By.XPATH,"//input[@placeholder='请输入密码']"),password)
        sel_click(driver, (By.XPATH,"//input[@value='登录']"))
        '''


        #写法三： 优化集成
        driver = open_homepage
        Event().event_login(driver,username,password)


        #sleep(1)
        if "欢迎您" in result:
            #text = driver.find_element(By.XPATH, "//div[@class='login_btn fl']").text           # 获取信息; 用户是否已经登录                                                        #打印信息
            #driver.find_element(By.XPATH,"//a[contains(text(),'退出')]").click()                 #点击退出按钮

            text = driver.get_text((By.XPATH, "//div[@class='login_btn fl']"))
            driver.sel_click((By.XPATH,"//a[contains(text(),'退出')]"))
            assert text == result

        elif "用户名错误" in result:
            #text = driver.find_element(By.XPATH, "//div[@class='user_error']").text  # 获取错误信息; 用户不存在
            #assert text == "用户名错误"
            text = driver.get_text((By.XPATH, "//div[@class='user_error']"))
            assert text == result

        elif "密码错误" in result:
            #text = driver.find_element(By.XPATH, "//div[@class='pwd_error']").text  # 获取错误信息; 密码错误
            #assert text == "密码错误"
            text = driver.get_text((By.XPATH, "//div[@class='pwd_error']"))
            assert text == result

        sleep(1)

    '''
    def test_shopping_mall_002(self,username,password,result):   # 测试用例2：用户不存在时，登录失败

        #——————————打开浏览器，最大化页面，然后隐式等待——————————
        # driver = webdriver.Chrome()           #实例化，打开了chrome浏览器，通过驱动
        # driver.get("http://127.0.0.1:8000/")  #打开一个浏览器地址; 打开网页
        # driver.maximize_window()              #窗口最大化
        # driver.implicitly_wait(10)            #隐式等待

        self.driver.get("http://127.0.0.1:8000/")

        self.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()          #根据xpath位置，然后点击登录按钮

        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys("bucunzai") #输入用户名
        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(username)

        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys("759667506")   #输入密码
        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(password)

        self.driver.find_element(By.XPATH,"//input[@value='登录']").click()                            #点击登录按钮
        sleep(2)

        text = self.driver.find_element(By.XPATH,"//div[@class='user_error']").text  #获取错误信息; 用户不存在
        #assert text == result
        assert text == '用户名错误'

    def test_shopping_mall_003(self,username,password,result):   # 测试用例3：用户名正确，密码错误，登录失败

        #——————————打开浏览器，最大化页面，然后隐式等待——————————
        # driver = webdriver.Chrome()           #实例化，打开了chrome浏览器，通过驱动
        # driver.get("http://127.0.0.1:8000/")  #打开一个浏览器地址; 打开网页
        # driver.maximize_window()              #窗口最大化
        # driver.implicitly_wait(10)            #隐式等待
        self.driver.get("http://127.0.0.1:8000/")

        self.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()          #根据xpath位置，然后点击登录按钮

        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys("test123456") #输入用户名
        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(username)

        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys("cuowumima")   #输入密码
        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(password)

        self.driver.find_element(By.XPATH,"//input[@value='登录']").click()                            #点击登录按钮
        sleep(2)

        text = self.driver.find_element(By.XPATH,"//div[@class='pwd_error']").text  #获取错误信息; 用户不存在
        #assert text == result
        assert text == '密码错误'
        #sleep(1)
    '''





'''
    def test_shopping_mall_004(self):   # 测试用例4：未注册的账号密码，注册成功

        #——————————打开浏览器，最大化页面，然后隐式等待——————————
        # driver = webdriver.Chrome()           #实例化，打开了chrome浏览器，通过驱动
        # driver.get("http://127.0.0.1:8000/")  #打开一个浏览器地址; 打开网页
        # driver.maximize_window()              #窗口最大化
        # driver.implicitly_wait(10)            #隐式等待

        self.driver.get("http://127.0.0.1:8000/")                                          #重新打开网页


        self.driver.find_element(By.XPATH,"//a[contains(text(),'注册')]").click()

        self.driver.find_element(By.XPATH,"//input[@id='user_name']").send_keys("test123457")        #输入注册用户名

        self.driver.find_element(By.XPATH,"//input[@id='pwd']").send_keys("zhucedenglu")   #输入注册密码

        self.driver.find_element(By.XPATH,"//input[@id='cpwd']").send_keys("zhucedenglu")               #输入确认密码

        self.driver.find_element(By.XPATH,"//input[@id='email']").send_keys('zhuce@qq.com')            #输入注册邮箱

        self.driver.find_element(By.XPATH,"//input[@value='注 册']").click()                            #点击注册按钮
        #sleep(2)

        #self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys("test123457") #不用重新输入用户名；注册会保存
        #sleep(1)
        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys("zhucedenglu") #验证输入密码
        sleep(1)
        #text = self.driver.find_element(By.XPATH,"//div[@class='pwd_error']").text  #获取错误信息; 用户不存在
        #print(text)                                                             #打印错误信息
        #sleep(3)
        #断言
        #assert text == "密码错误"
        #driver.find_elements(By.XPATH)  #加上s 就是查找列表的意思
'''