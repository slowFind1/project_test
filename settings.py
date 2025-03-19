
from time import sleep
import pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By

class Environment:

    #被测试环境，网页 或者 andirons端
    #URL = ""
    url = "http://127.0.0.1:8000/"

    #自动化测试，默认一个的用户和密码
    username = "test1234567"
    password = "759667506"
    cpwd = "759667506"
    email = "test1234567@qq.com"


class DBSql:
    sql_file = rf'E:\DOCUMENT\Web_ui\TIantian_html\daily_fresh_demo-master\db.sqlite3' #数据库文件,天天生鲜文件夹下，数据集文件
    # sql_list = [
    #     'DELETE FROM df_order_orderdetailinfo;',     #删除订单的详细信息
    #     'DELETE FROM df_order_orderinfo;',           #删除订单
    #     'delete from df_user_userinfo;',            #删除用户
    #     'delete from df_cart_cartinfo;'              #删除购物车
    #     #输入测试内容语句：类似40, 'test1', 'b444ac06613fc8d63795be9ad0beaf55011936ac', '898787869@qq.com', 'test1', '广州市天河区棠下东街101号', '12345678989', '51200'
    #     #"INSERT INTO 'df_user_userinfo' VALUES ('46', 'test123456', 'fb15a1bc44e13e2c58a0a502c74a54106b5a0dc', 'sadfasdfasd@qq.com','','','','' ) "
    #     "INSERT INTO 'df_user_userinfo' VALUES ('46', 'test123456', 'fb15a1bc44e13e2c58a0a502c74a54106b5a0dc','sadfasdfasd@qq.com','','','','' );"
    #
    # ]
    sql_list = [
        "DELETE FROM df_order_orderdetailinfo",
        "DELETE FROM df_order_orderinfo",
        "DELETE FROM df_user_userinfo",
        "DELETE FROM df_cart_cartinfo",
        "INSERT INTO df_user_userinfo VALUES ('40', 'test1234567', '8af362b9b445502a4991a56a15fc0e954412ffef', 'test1234567@qq.com', '', '', '', '')"
    ]