#事件动作代码，封装一些常用的动作，登录，注册，购买下单等
from time import sleep

import allure
import pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By

from common.log import log
from common.selenium_common import sel_click,element_visible,element_clickable,send_keys,get_text
from common.sql import MysqlAuto
#from conftest import open_page
from settings import Environment


class Event:

    @staticmethod
    @allure.step("登录") # 测试报告需要用到
    def event_login(driver,username,password):  # 登录事件
        #driver = open_page()
        try:
            driver.get(Environment.url)  #确保每次都是进入首页
            driver.sel_click( (By.XPATH, "//a[contains(text(),'登录')]"))
            driver.send_keys( (By.XPATH, "//input[@placeholder='请输入用户名']"), username)
            driver.send_keys( (By.XPATH, "//input[@placeholder='请输入密码']"), password)
            driver.sel_click( (By.XPATH, "//input[@value='登录']"))
        except Exception as e:
            print(f"登录失败，异常为：{e}")
            log.error(f"登录失败,异常为{e}")
            raise e


    @staticmethod
    @allure.step("注册")#注册事件,测试报告需要用到
    def event_register(driver,username,password,cpwd,email):   # 注册事件
        #driver = open_page()
        try:
            driver.get(Environment.url) #确保每次都是进入首页
            driver.sel_click((By.XPATH, "//a[contains(text(),'注册')]"))  # 调用selenium封装内容，点击注册按钮
            driver.send_keys((By.XPATH, "//input[@id='user_name']"), username)
            driver.send_keys((By.XPATH, "//input[@id='pwd']"), password)
            driver.send_keys((By.XPATH, "//input[@id='cpwd']"), cpwd)
            driver.send_keys((By.XPATH, "//input[@id='email']"), email)
            driver.sel_click((By.XPATH, "//input[@value='注 册']"))
        except Exception as e:
            print(f"注册失败，异常为：{e}")
            log.error(f"注册失败,异常为{e}")
            raise e


    @staticmethod
    @allure.step("立即购买并点击提交订单")
    def event_submit_order(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]")) #选择商品牛奶草莓
            driver.sel_click((By.XPATH, "//a[@id='buy_now']"))             #立即购买
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))  #结算按钮
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))           #提交订单
            sleep(1)
        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e

    @staticmethod
    @allure.step("新增加收获地址")
    #def add_address(driver,name='张三',phone=’12345678901',province='北京',city='北京',area='东城区',detail='北京东城区',address):
    def add_address(driver, name='张三',phone='12345678901',Postcode='998989',address='北京东城区'):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//a[contains(text(),'用户中心')]"))                 # 点击用户中心
            driver.sel_click((By.XPATH, "//a[contains(text(),'· 收货地址')]"))               # 点击收获地址进行添加新地址
            driver.send_keys((By.XPATH, "//input[@name='ushou']"), name)                   # 收件人
            driver.send_keys((By.XPATH, "//input[@name='uphone']"), phone)                 # 电话
            driver.send_keys((By.XPATH, "//input[@name='uyoubian']"), Postcode)            # 邮编
            driver.send_keys((By.XPATH, "(//textarea[@name='uaddress'])[1]"), address)     # 详细地址
            driver.sel_click((By.XPATH, "//input[@value='修改地址']"))                       # 提交地址
            #driver.sel_click((By.XPATH, "//a[@id='order_btn']"))                           # 提交订单
            sleep(1)

        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e

    @staticmethod
    @allure.step("购物车一个商品")
    # def add_address(driver,name='张三',phone=’12345678901',province='北京',city='北京',area='东城区',detail='北京东城区',address):
    def event_add_cart(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]"))  # 选择商品牛奶草莓
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

            driver.sel_click((By.XPATH, "//a[@class='cart_name fl']"))                    # 点击购物车
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))                 # 结算按钮
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))                         # 提交订单
            sleep(1)
        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e

    @staticmethod
    @allure.step("购物车多个商品")
    # def add_address(driver,name='张三',phone=’12345678901',province='北京',city='北京',area='东城区',detail='北京东城区',address):
    def event_add_carts_more(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]"))  # 选择商品牛奶草莓
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[2]/a[1]"))  # 选择商品海南香蕉
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

            driver.get(Environment.url) #进入首页
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[4]/a[1]"))  # 选择商品海南香蕉
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))  # 加入购物车

            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//a[@class='cart_name fl']"))  # 点击购物车
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))  # 结算按钮
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))  # 提交订单
            sleep(1)
        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e

    @staticmethod
    @allure.step("购物车0个商品")
    # def add_address(driver,name='张三',phone=’12345678901',province='北京',city='北京',area='东城区',detail='北京东城区',address):
    def event_add_cart_0(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//div[@class='user_link fl']//a[contains(text(),'我的购物车')]"))  # 点击我的购物车
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))   # 结算按钮
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))            # 提交订单
            sleep(1)
        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e


    @staticmethod
    @allure.step("添加购物车商品")
    def event_add_cart_goods(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//body[1]/div[5]/div[2]/ul[1]/li[1]/a[1]"))  # 选择商品牛奶草莓
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))     # 加入购物车
            driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))     # 加入购物车
            #driver.sel_click((By.XPATH, "(//a[contains(text(),'加入购物车')])[1]"))     # 加入购物车
            #sleep(5)  # 增加等待时间，确保商品添加成功
            #text = driver.get_text((By.XPATH, "(//div[@id='show_count'])[1]"))        # 点击查看购物车
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//a[@class='cart_name fl']"))               # 点击查看购物车

        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e


    @staticmethod
    @allure.step("提交购物车商品")
    def event_submit_cart_goods(driver):
        try:
            driver.get(Environment.url)
            driver.sel_click((By.XPATH, "//div[@class='user_link fl']//a[contains(text(),'我的购物车')]"))  # 点击我的购物车
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))  # 点击去结算;
            driver.sel_click((By.XPATH, "(//a[contains(text(),'提交订单')])[1]"))  # 点击提交订单

        except Exception as e:
            print(f"提交订单失败，异常为：{e}")
            raise e

    @staticmethod
    @allure.step("搜索商品")
    def event_search_goods(driver,goods):
        try:
            driver.get(Environment.url)
            driver.send_keys((By.XPATH,"//input[@placeholder='搜索商品']"),goods) # 输入搜索商品
            driver.sel_click((By.XPATH,"//input[@value='搜索']"))                # 点击搜索按钮
            # driver.send_keys((By.XPATH, "//input[@id='q']"), goods)
            # driver.sel_click((By.XPATH, "//button[@id='s_btn']"))
        except Exception as e:
            print(f"搜索商品失败，异常为：{e}")
            raise e