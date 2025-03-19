from time import sleep

import allure
import pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By
from common.selenium_common import sel_click,element_visible,element_clickable,send_keys,get_text
from common.sql import MysqlAuto
from settings import Environment, DBSql
from  po.event import Event
#——————————————————————————————————测试注册用例
class TestRegister:

    @allure.feature("登录注册")
    @allure.story("注册")
    def  test_shopping_mall_004(self,open_homepage): #未注册的账号，注册成功

        username = 'test_shopping_004'
        password = "test_shopping_004"
        cpwd = "test_shopping_004"
        email = "test_shopping_004@qq.com"

        driver = open_homepage
        Event.event_register(driver,username,password,cpwd,email)


        #因为数据库事先执行了清除命令，只有自己设置的数据存放数据库中，所以不用担心重复注册
        # sel_click(driver,(By.XPATH,"//a[contains(text(),'注册')]"))  #调用selenium封装内容，点击注册按钮
        # send_keys(driver,(By.XPATH,"//input[@id='user_name']"),username)
        # send_keys(driver,(By.XPATH,"//input[@id='pwd']"),password)
        # send_keys(driver,(By.XPATH,"//input[@id='cpwd']"),cpwd)
        # send_keys(driver,(By.XPATH,"//input[@id='email']"),email)
        # sel_click(driver,(By.XPATH,"//input[@value='注 册']"))

        # driver.sel_click((By.XPATH,"//a[contains(text(),'注册')]"))  #调用selenium封装内容，点击注册按钮
        # driver.send_keys((By.XPATH,"//input[@id='user_name']"),username)
        # driver.send_keys((By.XPATH,"//input[@id='pwd']"),password)
        # driver.send_keys((By.XPATH,"//input[@id='cpwd']"),cpwd)
        # driver.send_keys((By.XPATH,"//input[@id='email']"),email)
        # driver.sel_click((By.XPATH,"//input[@value='注 册']"))

        '''
        检测用户是否注册成功：
            1.检测数据库，查询用户表，是否存在
            2.直接用此账号进行登录，是否可以登录成功
        '''
        #1.验证数据库是否存在用户名
        # sql = [f'select * from df_user_userinfo where uname ="{username}"']
        # result =  MysqlAuto().execute_sql(sql)
        # assert  username in result[0]

        result = MysqlAuto().execute_sql([f'select * from df_user_userinfo where uname ="{username}"'])[0]
        assert  username in result

        #2.验证登录是否正常
        # send_keys(driver, (By.XPATH, "//input[@placeholder='请输入用户名']"), username)
        # send_keys(driver, (By.XPATH, "//input[@placeholder='请输入密码']"), password)
        # sel_click(driver, (By.XPATH, "//input[@value='登录']"))

        Event().event_login(driver,username,password)   #调用封装好的登录操作驱动，进行登录

        text = driver.get_text((By.XPATH, "//div[@class='login_btn fl']"))  # 获取错误信息; 用户不存在                                                         #打印信息
        driver.sel_click((By.XPATH, "//a[contains(text(),'退出')]"))      # 点击退出按钮
        #print(text)
        assert text == f"欢迎您：{username} | 退出"

        sleep(1)

    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_005(self,open_homepage): #测试已经存在的账号，登录失败
        username = 'test1234567'
        password = "759667506"
        cpwd = "759667506"
        email = "test1234567@qq.com"

        driver = open_homepage
        Event.event_register(driver,username,password,cpwd,email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'用户名已经存在')]"))
        assert  text =='用户名已经存在'

    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_006(self, open_homepage):  # 注册时，密码为空
        username = 'test_shopping_004'
        password = " "
        cpwd = "test_shopping_004"
        email = "test_shopping_004@qq.com"

        driver = open_homepage
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'密码最少4位，最长20位')]"))
        assert text == '密码最少4位，最长20位'


    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_007(self, open_homepage):  # 注册时，邮箱为空
        username = 'test_shopping_004'
        password = "test_shopping_004"
        cpwd = "test_shopping_004"
        email = " "

        driver = open_homepage
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'你输入的邮箱格式不正确')]"))
        assert text == '你输入的邮箱格式不正确'


    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_008(self, open_homepage):  # 注册时，两次密码不一致
        MysqlAuto().execute_sql(DBSql.sql_list)

        username = 'test_shopping_004'
        password = "test_shopping_004"
        cpwd = "test_shopping_008"
        email = "test_shopping_004@qq.com"

        driver = open_homepage
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'两次输入的密码不一致')]"))
        assert text == '两次输入的密码不一致'



    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_009(self, open_homepage):  # 注册时，密码少于4位
        MysqlAuto().execute_sql(DBSql.sql_list)

        username = 'test_shopping_004'
        password = "t"*3
        cpwd = "t"*3
        email = "test_shopping_004@qq.com"

        driver = open_homepage
        MysqlAuto().execute_sql(DBSql.sql_list)
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'密码最少4位，最长20位')]"))
        assert text == '密码最少4位，最长20位'



    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_010(self, open_homepage):  # 注册时，密码超过20位
        username = 'test_shopping_004'
        password = "t"*21
        cpwd = "t"*21
        email = "test_shopping_004@qq.com"

        driver = open_homepage
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'密码最少4位，最长20位')]"))
        assert text == '密码最少4位，最长20位'

    @allure.feature("登录注册")
    @allure.story("注册")
    def test_shopping_mall_011(self, open_homepage):  # 注册时，邮箱格式不正确
        username = 'test_shopping__004'
        password = "test_shopping__004"
        cpwd = "test_shopping__004"
        email = " "

        driver = open_homepage
        Event.event_register(driver, username, password, cpwd, email)

        text = driver.get_text((By.XPATH, "//span[contains(text(),'你输入的邮箱格式不正确')]"))
        assert text == '你输入的邮箱格式不正确'



    @allure.feature("登录注册")
    @allure.story("退出")
    def test_shopping_mall_012(self, open_homepage):   # 测试退出功能

        driver = open_homepage
        Event.event_login(driver, Environment.username, Environment.password)  # 调用封装好的登录操作驱动，进行登录
        driver.sel_click((By.XPATH,"//a[contains(text(),'退出')]"))             # 点击退出按钮
        sleep(1)
        # text = driver.get_text((By.XPATH, "//a[contains(text(),'登录')]"))    #只获取登录所在的区域
        # assert text == '登录'
        text = driver.get_text((By.XPATH,"(//div[@class='login_btn fl'])[1]"))  #获取登录和注册所在的区域
        assert  text == '登录 | 注册'

    @allure.feature("订单提交")
    @allure.story("立即购买成功")
    def test_shopping_mall_013(self, login):        #立即购买，订单提交成功

        driver = login                      # 调用封装好的登录操作驱动，进行登录

        MysqlAuto().execute_sql(DBSql.sql_list)  #预防所有测试用例执行时候，数据库数据未被清零

        Event.add_address(driver)           # 添加地址
        Event.event_submit_order(driver)    # 提交订单


        # text = driver.alert_text()
        # assert  text == '订单提交成功'


        #查询数据库，进行验证是否存在数据存储
        sql = ['select * from df_order_orderinfo']
        order_list = MysqlAuto().execute_sql(sql)
        assert  len(order_list) == 1

        #并验证是否此id是新创建的
        order_id = order_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert  order_id in text



    @allure.feature("订单提交")
    @allure.story("立即购买，无收获地址")
    def test_shopping_mall_014(self, login):  # 立即购买，订单提交失败;无收获地址

        driver = login
        MysqlAuto().execute_sql(DBSql.sql_list)  #预防所有测试用例执行时候，数据库数据未被清零

        Event.event_submit_order(driver)
        text = driver.alert_text()
        assert  text == '请填写正确的收货地址'

    @allure.feature("订单提交")
    @allure.story("一个商品加入购物车，提交成功")
    def test_shopping_mall_015(self, login): # 一个商品加入购物车，订单提交成功
        driver = login
        MysqlAuto().execute_sql(DBSql.sql_list)  #预防所有测试用例执行时候，数据库数据未被清零

        Event.add_address(driver)
        #Event.event_submit_order(driver)
        Event.event_add_cart(driver)


        # text = driver.alert_text()
        # assert  text == '订单提交成功'
        # 查询数据库，进行验证是否购买成功
        sql = ['select * from df_order_orderinfo']
        order_list = MysqlAuto().execute_sql(sql)
        assert len(order_list) ==1

        # 并验证是否此id是新创建的
        order_id = order_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert order_id in text



    @allure.feature("订单提交")
    @allure.story("多个商品加入购物车，订单提交成功")
    def test_shopping_mall_016(self, login):  # 多个商品加入购物车，订单提交成功
        driver = login
        MysqlAuto().execute_sql(DBSql.sql_list)  # 预防所有测试用例执行时候，数据库数据未被清零

        Event.add_address(driver)            # 添加地址
        # Event.event_submit_order(driver)
        Event.event_add_carts_more(driver)

        sql = ['select * from df_order_orderinfo']
        order_list = MysqlAuto().execute_sql(sql)
        assert len(order_list) == 1

        # 并验证是否此id是新创建的
        order_id = order_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert order_id in text




    @allure.feature("订单提交")
    @allure.story("加入购物车，订单提交失败")
    def test_shopping_mall_017(self, login):  # 0个商品加入购物车，订单提交失败
        driver = login
        Event.add_address(driver)            # 添加地址
        # Event.event_submit_order(driver)

        Event.event_add_cart_0(driver)       # 直接0个商品去结算
        text = driver.alert_text()
        assert text == '订单提交失败'



    '''
        思考： 在此搜索测试，是否将网页的全部内容都测试，搜索一遍，那么所有内容怎么集成，一个excel表？还是字典文件
    
    '''

    @allure.feature("搜索")
    @allure.story("搜索存在的商品成功")
    def test_shopping_mall_018(self, open_homepage):  # 搜索存在的商品进行搜索
        driver = open_homepage

        # driver.send_keys((By.XPATH,"//input[@placeholder='搜索商品']"),"牛奶草莓")
        # driver.sel_click((By.XPATH,"//input[@value='搜索']"))
        # text = driver.get_text((By.XPATH,"//a[contains(text(),'牛奶草莓')]"))
        # assert text == '牛奶草莓'

        keyword = {'草莓','香蕉','刀鱼','扇贝','基围虾','葡萄'}
        for i in keyword:
            Event.event_search_goods(driver,i)
            text = driver.get_text((By.XPATH,"//ul[@class='goods_type_list clearfix']"))
            assert  i in text

    @allure.feature("搜索")
    @allure.story("搜索不存在的商品失败")
    def test_shopping_mall_019(self, open_homepage):  # 搜索不存在的商品进行搜索
        driver = open_homepage
        driver.send_keys((By.XPATH,"//input[@placeholder='搜索商品']"),"超级无敌大草莓")
        driver.sel_click((By.XPATH,"//input[@value='搜索']"))
        # text = driver.get_text((By.XPATH,"//a[contains(text(),'牛奶草莓')]"))
        text = driver.alert_text()
        assert text == '您的查询结果为空，为您推荐以下商品'

    @allure.feature("搜索")
    @allure.story("搜索空白")
    def test_shopping_mall_020(self, open_homepage):  # 搜索空白进行搜索
        driver = open_homepage
        driver.send_keys((By.XPATH,"//input[@placeholder='搜索商品']"),"")
        driver.sel_click((By.XPATH,"//input[@value='搜索']"))
        # text = driver.get_text((By.XPATH,"//a[contains(text(),'牛奶草莓')]"))
        text = driver.alert_text()
        assert text == '请输入搜索内容'

    @allure.feature("我的订单")
    @allure.story("检查我的订单页面是否正常显示")
    def test_shopping_mall_021(self, login):  # 检查我的订单页面是否正常显示
        driver = login

        #driver.sel_click((By.XPATH,"//a[contains(text(),'我的订单')]"))
        #除了上述点击之外，还可以直接打开对应网页
        driver.get(Environment.url + 'user/order/1')


        # text = driver.get_text((By.XPATH,"//h3[contains(text(),'全部订单')]"))
        # assert text == '全部订单'
        text = driver.get_text((By.XPATH,"//div[@class='pagenation']"))
        assert  text == '1'

    @allure.feature("购物车")
    @allure.story("商品加入购物车正常")
    def test_shopping_mall_022(self, login):  # 商品加入购物车正常
        driver = login
        #driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]"))  # 选择商品牛奶草莓
        driver.get(Environment.url + '18/')
        driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
        driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

        driver.sel_click((By.XPATH, "//a[@class='cart_name fl']"))             # 点击查看购物车

        text = driver.get_text((By.XPATH,"//li[contains(text(),'牛奶草莓')]"))
        assert  '牛奶草莓' in text



    @allure.feature("购物车")
    @allure.story("商品加入购物车,并增加商品数量")
    def test_shopping_mall_023(self, login):  # 商品加入购物车正常
        driver = login
        MysqlAuto().execute_sql(DBSql.sql_list)  # 预防所有测试用例执行时候，数据库数据未被清零

        #driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]"))  # 选择商品牛奶草莓
        driver.get(Environment.url + '18/')

        driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
        driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

        driver.sel_click((By.XPATH, "//a[@class='cart_name fl']"))            # 点击购物车
        pre = int(float(driver.get_text((By.XPATH,"//em[@id='total']"))))     # 获取商品金额

        driver.sel_click((By.XPATH, "//a[contains(text(),'+')]"))             # 增加商品数量
        suf = int(float(driver.get_text((By.XPATH,"//em[@id='total']"))))     # 获取商品金额
        assert suf == pre*2

    @allure.feature("购物车")
    @allure.story("商品加入购物车,并减少商品数量")
    def test_shopping_mall_024(self, login):
        driver = login
        MysqlAuto().execute_sql(DBSql.sql_list)  # 预防所有测试用例执行时候，数据库数据未被清零

        Event.event_add_cart_goods(driver)  # 加入购物车一个商品

        driver.sel_click((By.XPATH, "//a[contains(text(),'+')]"))        # 增加商品数量,以防数量为1不能减
        pre = int(float(driver.get_text((By.XPATH,"//em[@id='total']"))))   # 获取商品数量
        #print(pre)


        driver.sel_click((By.XPATH, "(//a[normalize-space()='-'])[1]")) # 减少商品数量

        suf = int(float(driver.get_text((By.XPATH,"//em[@id='total']"))))  # 获取商品数量
        #print(suf)
        assert suf *2 ==  pre

    @allure.feature("购物车")
    @allure.story("购物车内,删除商品")
    def test_shopping_mall_025(self, login): # bug ：点击添加购物车商品后，未成功添加，有延迟
        driver = login

        Event.event_add_cart_goods(driver)  # 加入购物车一个商品

        #检查购物车商品是否存在
        driver.get(Environment.url + 'cart/') #进入购物车界面
        text = driver.get_text((By.XPATH,"(//b[@class='total_count1'])[1]"))  #检查数量
        assert  text == '1'


        driver.sel_click((By.XPATH, "//a[contains(text(),'删除')]"))  # 点击删除按钮
        driver.click_alert()    # 点击确认删除

        '''
        driver.sel_click((By.XPATH, "(//a[contains(text(),'我的购物车')])[1]"))  #刷新页面
        sign = driver.element_visible((By.XPATH, "(//li[contains(text(),'牛奶草莓')])[1]")) # 判断是否删除成功

        #若是selenium：  def element_visible(self,  by,sel, timeout=30): 那么需要下面代码
        #sign = driver.element_visible(By.XPATH, "(//li[contains(text(),'牛奶草莓')])[1]")
        assert  sign == False
        '''

        #删除后检查是否数量为0
        text = driver.get_text((By.XPATH, "(//b[@class='total_count1'])[1]"))
        assert  text == '0'


    @allure.feature("购物车")
    @allure.story("购物车,商品数量为0")
    def test_shopping_mall_026(self, login):
        driver = login
        Event.add_address(driver)

        # driver.get(Environment.url)
        # driver.sel_click((By.XPATH, "//div[@class='user_link fl']//a[contains(text(),'我的购物车')]")) # 点击我的购物车
        # driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))         # 点击去结算;
        # driver.sel_click((By.XPATH, "(//a[contains(text(),'提交订单')])[1]"))   # 点击提交订单

        Event.event_submit_cart_goods(driver)
        text =driver.alert_text()
        assert  text == '订单提交失败'

    @allure.feature("收货地址")
    @allure.story("输入收货地址")
    def test_shopping_mall_027(self, login):
        driver = login
        Event.add_address(driver)

        text = driver.get_text((By.XPATH, "(//dt[contains(text(),'收件人：张三')])[1]"))
        assert text == '收件人：张三'
