import os
import  time
import  re
from  time import  sleep
import  allure
#from selenium.webdriver.chrome import webdriver
from  selenium import  webdriver
from  selenium.webdriver.support import  expected_conditions as EC
from  selenium.webdriver.support.wait import WebDriverWait
from  common.log import  log
from common.sql import  MysqlAuto
from config.conf import  ALLURE_IMG_DIR
from settings import DBSql, Environment


class Base:
    def __init__(self,driver=None):
        ''''''
        '''
        
                初始化driver； 清楚数据库数据，封装了selenium操作层（第三层）; 不用特定调用selenium_common库中动作
                直接调用dirver.sel_click() 动作即可，都封装再Base中，在封装在HomePage中
        
        '''
        if driver:
            self.driver = driver
        else:
            #那么进行首次打开网页
            #self.driver = webdriver.Firefox()  #需要对应版本的驱动
            self.driver = webdriver.Chrome()
            #self.driver.get(Environment.url)
            self.driver.implicitly_wait(10) #隐式等待
            self.driver.maximize_window()

            #初始化数据
            MysqlAuto().execute_sql(DBSql.sql_list)

    # 打开网页
    def get(self,url):

        try:
            self.driver.get(url)
            return self.driver
        except Exception as e:
            log.error(f"打开网页失败，异常为：\n{e}")
            raise e

    # 关闭浏览器
    def quit(self):

        try:
            self.driver.quit()
        except Exception as e:
            log.error(f"关闭浏览器失败，异常为：\n{e}")
            raise e


    # 获取弹窗文本
    def alert_text(self):
        try:
            alert = self.driver.switch_to.alert
            # 获取弹窗文本
            text = alert.text
            log.info(f"获取到弹窗文本为：{text}")
            alert.accept()
            return text
        except Exception as e:
            log.error(f"获取弹窗文本失败，异常为：\n{e}")
            raise e

    #点击弹窗
    def click_alert(self):
        try:
            # 获取弹窗
            alert = self.driver.switch_to.alert
            # 点击弹窗按钮； 点击确认按钮
            alert.accept()
        except Exception as e:
            log.error(f"点击弹窗失败，异常为：\n{e}")
            raise e

    @allure.step("鼠标左键点击")
    def sel_click(self,sel, timeout=20): #sel : selement 元素
        # print("鼠标左键点击")
        # expected_conditions.
        try:
            # drive.find_element(By.XPATH,sel).click()
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((sel))).click()
            # log.info("元素定位成功")
            sleep(0.2)

            selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))  # 过滤掉特殊字符，去找里面的中文
            if len(selen) > 0:
                # allure.attach(selen,"元素定位成功")
                log.debug(f"点击元素:{selen}")
            return True

        except Exception as e:
            log.error(f"元素定位失败,无法定位该元素：{sel},异常为：\n{e}")
            raise e

    @allure.step("元素可点击")
    def element_clickable(self, by, sel, timeout=30):
        # print("元素可点击")
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, sel)))
            log.debug("元素可点击")
            return True
        except Exception as e:
            log.error(f"已超出超时{timeout}秒，【{sel}】仍然未加载出，不可点击,异常为：\n{e}")
            raise e

    @allure.step("元素是否可见且存在出现")
    def element_visible(self,  sel, timeout=30):
        # print("元素可见")

        # try:
        #     WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, sel)))
        #     log.debug("元素可见")
        #     return True
        # except Exception as e:
        #     # log.error(f"已超出超时{timeout}秒，【{sel}】仍然未加载出,不可见,异常为：\n{e}")
        #     # raise e
        #     return  False

        try:
            elements = self.driver.find_elements((sel))
            if len(elements) == 0:
                log.warning(f"元素【{sel}】不存在")
                return False  # 说明元素根本不存在

            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((sel)))
            selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))  # 过滤掉特殊字符，去找里面的中文
            if len(selen) > 0:
                log.debug(f"元素【{selen}】可见")
            return True  # 说明元素存在且可见
        except Exception as e :
            log.warning(f"元素【{sel}】在 {timeout} 秒内不可见，可能已删除")
            #return False  # 说明元素不可见（可能被删除）
            raise e

    @allure.step("输入内容")
    def send_keys(self, sel, value, timeout=30):  # 输入内容: 浏览器 ，元素selement ， 值， 超时时间
        # print("输入内容")
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((sel))).clear()  # 清空输入框，以防有上一个报存值
            sleep(0.2)
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((sel))).send_keys(value)
            sleep(0.2)
            selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))
            if len(selen) > 0:
                log.debug(f"点击：{selen}，并输入值：{value}")
            return True

        except Exception as e:
            log.error(f"已超出超时{timeout}秒，无法定位该元素【{sel}】,异常为：\n{e}")
            raise e

    @allure.step("获取元素text文本值")
    def get_text(self, els, timeout=10, mode=0):
        # print("获取元素text文本值")
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((els)))
            if mode == 0:
                log.debug(element.text)
                return element.text
            elif mode == 1:
                log.debug(element.get_attribute("textContent"))
                return element.get_attribute("textContent")
            # selen = re.sub('[^\u4e00-\u9fa5]+','',str(sel))
            # if len(selen)  > 0:
            #     log.info(f"获取元素：{selen}，text文本值：{text}")
            # return text

        except Exception as e:
            log.error(f"已超出超时{timeout}秒，无法定位该元素【{els}】,异常为：\n{e}")
            raise e

    @allure.step("获取value值")
    def get_value(self,  sel, timeout=10, mode=0):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((sel)))

            # 如果是输入框，获取 value
            if element.tag_name == "input":
                text = element.get_attribute("value")
            else:
                text = element.text if mode == 0 else element.get_attribute("textContent")

            log.debug(f"获取元素【{sel}】文本值：{text}")
            return text
        except Exception as e:
            log.error(f"已超出超时{timeout}秒，无法定位该元素【{sel}】,异常为：\n{e}")
            raise e


    #@allure.step("获取失败截图")
    def allure_save_screenshot(self,name):

        with open(self.chrom_save_screenshot(), 'rb') as f:
            log.debug("已保存失败截图")
            allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.PNG)
            #allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

        return True


    @allure.step("chrome自带截图")
    def chrom_save_screenshot(self):
        try:
            img_dir = ALLURE_IMG_DIR
            str_time = str(time.time())[:10]
            img_file = img_dir + f'\\temp_chrom_save_screenshot_{str_time}.png' # 截图文件路径
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
                log.info(f'创建目录:{img_dir}')
            sleep(1)
            self.driver.save_screenshot(img_file)   # 截图报错
            return img_file

        except Exception as e:
            log.error("截图失败")
            raise



        #     # 截图
        #     self.driver.get_screenshot_as_file(f"{ALLURE_IMG_DIR}/{time.strftime('%Y%m%d%H%M%S')}.png")
        #     log.debug("已保存失败截图")
        #     return f"{ALLURE_IMG_DIR}/{time.strftime('%Y%m%d%H%M%S')}.png"
        # except Exception as e:
        #     log.error("保存失败截图失败, 异常: \n{e}")
        #     raise e