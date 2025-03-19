# 文件路径等设置； 环境路径设置； 若是将此文件移植到另一个位置 ，那么此输出也会改变
# 基础配置文件config；  若是单独测试，需要调用在conftest中进行修改； 然后输出到日志文件
import  os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) #获取当前文件路径
LOG_DIR = os.path.join(BASE_DIR,'logs')
ALLURE_IMG_DIR = os.path.join(LOG_DIR,'image_allure') #截图路径,allure报告截图路径

if __name__ == '__main__':
    print(BASE_DIR)
    print(LOG_DIR)
    print(ALLURE_IMG_DIR)