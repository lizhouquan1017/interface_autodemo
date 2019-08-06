import unittest
from tools.HTMLTestRunner_PY3 import HTMLTestRunner
from tools.sendEmail import SendEmail
from tools.getToken import GetToken
import time


"""测试用例存放目录和测试报告存放目录"""
test_dir = './testcase'
report_dir = './report'
now = time.strftime("%Y-%m-%d %H_%M_%S")
report_name = report_dir + '/result_' + now + ".html"

"""覆盖所有用例"""
discover = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")


if __name__ == "__main__":
    GetToken().login()
    with open(report_name, "wb") as f:
        runner = HTMLTestRunner(stream=f, title='接口自动化测试报告', description='用例执行情况:')
        runner.run(discover)
        # SendEmail().send_report()
