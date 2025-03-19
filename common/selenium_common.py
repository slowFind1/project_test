import re
#from telnetlib import EC
from time import sleep
import  allure
import  pytest
from  selenium import  webdriver
from  selenium.webdriver.common.by import  By
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver import ActionChains
from common.log  import  log

@allure.step("鼠标左键点击")
#def sel_click(driver,sel,timeout=20):
def sel_click(driver, sel, timeout=20):
    #print("鼠标左键点击")
    #expected_conditions.
    try:
        #drive.find_element(By.XPATH,sel).click()
        WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((sel))).click()
        #log.info("元素定位成功")
        sleep(0.2)

        selen = re.sub('[^\u4e00-\u9fa5]+','',str(sel)) #过滤掉特殊字符，去找里面的中文
        if len(selen) > 0:
            #allure.attach(selen,"元素定位成功")
            log.debug(f"点击元素:{selen}")
        return True

    except Exception as e:
        log.error(f"元素定位失败,无法定位该元素：{sel},异常为：\n{e}")
        raise e


@allure.step("元素可点击")
def element_clickable(driver,by,sel,timeout=30):
    #print("元素可点击")
    try:
        WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((by,sel)))
        log.debug("元素可点击")
        return True
    except Exception as e:
        log.error(f"已超出超时{timeout}秒，【{sel}】仍然未加载出，不可点击,异常为：\n{e}")
        raise e


@allure.step("元素是否可见且存在出现")
def element_visible(driver,by,sel,timeout=30):
    #print("元素可见")
    try:
        WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((by,sel)))
        log.debug("元素可见")
        return True
    except Exception as e:
        log.error(f"已超出超时{timeout}秒，【{sel}】仍然未加载出,不可见,异常为：\n{e}")
        raise e


@allure.step("输入内容")
def send_keys(driver,sel,value,timeout=30):  # 输入内容: 浏览器 ，元素selement ， 值， 超时时间
    #print("输入内容")
    try:
        WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((sel))).clear() # 清空输入框，以防有上一个报存值
        sleep(0.2)
        WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((value))).send_keys(value)
        sleep(0.2)
        # element = WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((by,value)))
        # element.clear()
        # sleep(0.2)
        # element.send_keys(value)
        # sleep(0.2)
        selen = re.sub('[^\u4e00-\u9fa5]+','',str(sel))
        if len(selen)  > 0:
            log.debug(f"点击：{selen}，并输入值：{value}")
        return True

    except Exception as e:
        log.error(f"已超出超时{timeout}秒，无法定位该元素【{sel}】,异常为：\n{e}")
        raise e


@allure.step("获取元素text文本值")
def get_text(driver,by,value,timeout=10,mode=0):
    #print("获取元素text文本值")
    try:
        element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((by,value)))
        if mode ==0:
            log.debug(element.text)
            return element.text.strip()
        elif mode ==1:
            log.debug(element.get_attribute("textContent"))
            return element.get_attribute("textContent").strip()
        # selen = re.sub('[^\u4e00-\u9fa5]+','',str(sel))
        # if len(selen)  > 0:
        #     log.info(f"获取元素：{selen}，text文本值：{text}")
        # return text

    except Exception as e:
        log.error(f"已超出超时{timeout}秒，无法定位该元素【{value}】,异常为：\n{e}")
        raise e



@allure.step("滚动至元素可见")
def scroll_to_element(driver, by, selector):
    """滚动到指定元素"""
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, selector)))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        log.debug(f"滚动到元素 [{selector}]")
        return True
    except Exception as e:
        log.error(f"无法滚动到元素 [{selector}], 异常: \n{e}")
        raise e




@allure.step("鼠标悬停")
def hover_element(driver, by, selector):
    """鼠标悬停到指定元素"""
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, selector)))
        ActionChains(driver).move_to_element(element).perform()
        log.debug(f"鼠标悬停在元素 [{selector}] 上")
        return True
    except Exception as e:
        log.error(f"无法悬停到元素 [{selector}], 异常: \n{e}")
        raise e


@allure.step("切换 iframe") #切换 iframe另一个框架
def switch_to_iframe(driver, by, selector, timeout=10):
    """切换到 iframe"""
    try:
        iframe = WebDriverWait(driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((by, selector)))
        log.debug(f"已切换到 iframe [{selector}]")
        return True
    except Exception as e:
        log.error(f"切换 iframe [{selector}] 失败, 异常: \n{e}")
        raise e


@allure.step("切换到新标签页")
def switch_to_new_tab(driver):
    """切换到最新打开的标签页"""
    try:
        driver.switch_to.window(driver.window_handles[-1])
        log.debug("已切换到最新的标签页")
        return True
    except Exception as e:
        log.error("切换标签页失败, 异常: \n{e}")
        raise e


@allure.step("截取当前屏幕")
def take_screenshot(driver, filename="screenshot.png"):
    """截图当前页面"""
    try:
        driver.save_screenshot(filename)
        log.debug(f"已截取屏幕并保存为 {filename}")
        return True
    except Exception as e:
        log.error(f"截图失败, 异常: \n{e}")
        raise e

