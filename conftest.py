from time import sleep
import pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By
from common.log  import  log
from  common.sql import MysqlAuto
from po.event import Event
from po.home_page import HomePage
from settings import DBSql, Environment


# 测试用例的代码基础配置，网页，测试日志设置等 ； test_case所设置conftest
@pytest.fixture(scope="class")
def login():
    #"""
    #Logs in a user and returns the session cookie.
    #def setup_class(self):              # 类方法，在类开始时执行，只执行一次,只需要打开一次浏览器，然后运行下面的测试

    '''
    print("开始测试")
    driver = webdriver.Chrome()

    log.debug("开始测试:打开浏览器")                    #导入日志进行记录； 输出会显示此行所在的py文件和位置line
    #driver.get("http://127.0.0.1:8000/")
    driver.get(Environment.url)

    driver.maximize_window()
    log.debug("最大化浏览器")

    #初始化数据库
    mysql = MysqlAuto()
    mysql.execute_sql(DBSql.sql_list)

    #默认登录
    Event().event_login(driver,Environment.username,Environment.password)


    #隐式等待
    driver.implicitly_wait(10)
    yield driver

    driver.quit()
    log.debug("结束测试:关闭浏览器")


    ''' # 优化改进上述，将HomePage集成，然后调用

    #优化改进上述，将HomePage集成，然后调用
    global  driver
    driver = HomePage()
    Event.event_login(driver,Environment.username,Environment.password)
    yield  driver
    driver.quit()


@pytest.fixture(scope="class")
def open_page():
    print("开始测试")
    driver = webdriver.Chrome()
    log.debug("开始测试:打开浏览器")  # 导入日志进行记录； 输出会显示此行所在的py文件和位置line

    #driver.get("http://127.0.0.1:8000/")
    driver.get(Environment.url)
    driver.maximize_window()
    log.debug("最大化浏览器")

    # 初始化数据库
    mysql = MysqlAuto()
    mysql.execute_sql(DBSql.sql_list)

    # 隐式等待
    driver.implicitly_wait(10)
    yield driver

    driver.quit()
    log.debug("结束测试:关闭浏览器")


@pytest.fixture(scope="class")
def open_homepage():
    global  driver
    driver = HomePage()
    driver.get(Environment.url)
    yield  driver
    driver.quit()



@pytest.hookimpl( tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item, call): #捕获失败截图； 钩子
    # execute all other hooks to obtain the report object
    '''
    
    :param item:  测试用例
    :param call:  测试步骤
    :return: 
    '''#
    out = yield
    result = out.get_result()
    log.info(f"test report:{result}")
    log.info(f"execute time-consuming:{round(call.duration, 2)} second")
    if result.failed:
        try:
            log.info(f"error screenshot.")
            driver.allure_save_screenshot('error_screenshot')
            #log.info(f"error page source:")
        except Exception as e:
            log.error(f"error screenshot:{e}")
            pass
