import time
import os
import logging

# 获取今天日期
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# 获取上一级目录
parent_path = os.path.dirname(os.path.dirname(__file__))
# 生成一个log文件,并以"当日日期.log"形式命名
final_path = parent_path + '/log/interface_' + today + '.log'


# 开发一个日志系统，既要把日志输出到控制台，还要写入日志文件
class Logger(object):

    def __init__(self, log_name='interfaceTest', log_file=final_path):
        """
           指定保存日志的文件路径，以及调用文件
           将日志存入到指定的文件中
        """

        # 创建一个logger,设置logger记录器的默认级别为DEBUG(10)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件,设置处理器的级别为DEBUG(10)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台,设置处理器的级别为WARNING(20)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger


if __name__ == "__main__":
    logger = Logger().get_log()
    logger.warning('hello world')
