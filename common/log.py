import  logging
import  time
from  config.conf import  BASE_DIR
import  colorlog
import os


log_colors_config = {
    'DEBUG':   'white',
    'INFO':    'green',
    'WARNING': 'yellow',
    'ERROR':   'red',
    'CRITICAL': 'bold_red',
}

# 创建日志记录器 logger
log = logging.getLogger('log_name')  # 创建一个logger
log.setLevel(logging.DEBUG)

# 创建控制台处理器 Handler
console_handler = logging.StreamHandler()               # 创建一个handler，用于写入日志文件
console_handler.setLevel(logging.DEBUG)


# 创建文件处理器
daytime = time.strftime("%Y-%m-%d", time.localtime())   # 获取当前时间
path = BASE_DIR + '/log/'                               # 日志文件路径
if not os.path.exists(path):                            # 判断路径是否存在，不存在则创建
    os.makedirs(path)
filename = path + f'/run_log_{daytime}.log'             # 日志文件名
file_handler = logging.FileHandler(filename=filename,mode='a',encoding='utf-8')   # 创建一个handler，用于写入日志文件
#file_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)



#——————————————————- 设置级别，以最高级别为准
#log.setLevel(logging.DEBUG )             # 设置日志级别；这意味着所有 DEBUG 及以上级别的日志都会传递给 Handler。
# console_handler.setLevel(logging.DEBUG)  # 添加handler；这意味着所有 DEBUG 及以上级别的日志都会输出到控制台。
# file_handler.setLevel(logging.INFO)      # 添加handler；这意味着只有 INFO 及以上级别的日志会输出到文件。


#———————————— 输出格式
file_formatter = logging.Formatter(
    #'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    fmt = '[%(levelname)s][%(asctime)s.%(msecs)03d]: %(message)s %(filename)s -> %(funcName)s line:%(lineno)d',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

console_formatter = colorlog.ColoredFormatter(
    #格式设置如下，输出到控制台，levelname表示等级info，error等， 后面设置颜色
    fmt = '[%(levelname)s]%(log_color)s[%(asctime)s.%(msecs)03d]: %(message)s %(filename)s -> %(funcName)s line:%(lineno)d',
    datefmt = '%Y-%m-%d %H:%M:%S',
    log_colors = log_colors_config
)


file_handler.setFormatter(file_formatter)       #设置文本格式，根据上述建立的
console_handler.setFormatter(console_formatter) #设置控制台格式


if not log.handlers:
    log.addHandler(file_handler)
    log.addHandler(console_handler)

console_handler.close()
file_handler.close()


if __name__ == '__main__':
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')

