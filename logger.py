import logging

from logging import handlers

class logger(object):
    
    #日志级别关系映射
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    # logger 初始化
    def __init__(self, filename,when='D',backCount=3, consoleFmt='%(asctime)s - %(message)s',fileLogFmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
    
        # 获取模块 logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.level_relations.get('debug'))#设置日志级别
        
        # 屏幕输出（打印 info 及以上级别）
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(self.level_relations.get('info'))
        format_str = logging.Formatter(consoleFmt)#设置日志格式
        consoleHandler.setFormatter(format_str) #设置屏幕上显示的格式
        
        # 文件输出（打印包含 debug 的所有级别）
        fileHandler = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        fileHandler.setLevel(self.level_relations.get('debug'))
        format_str = logging.Formatter(fileLogFmt)#设置日志格式
        fileHandler.setFormatter(format_str)#设置文件里写入的格式
        
        # 注册 handlers
        self.log.addHandler(consoleHandler)
        self.log.addHandler(fileHandler)
        
if __name__ == '__main__':
    # TEST
    log = logger('all.log')  