# coding = utf-8

import configparser
from os import path


parent_path = path.dirname(path.dirname(__file__))
final_path = path.join(parent_path, "testFile\data.ini")


class ReadData(object):
    """ 读取cfg.ini文件，返回各个参数值构成的字典"""
    def __init__(self):
        self.cof = configparser.ConfigParser()
        self.cof.read(final_path, encoding='utf-8')

    def get_api_info(self):
        api_dict = dict()
        api_dict['base_url'] = self.cof.get('api', 'base_url')
        api_dict['Authorization'] = self.cof.get('api', 'Authorization')
        api_dict['loginname'] = self.cof.get('api', 'loginname')
        api_dict['code'] = self.cof.get('api', 'code')
        api_dict['authorization'] = self.cof.get('api', 'authorization')
        return api_dict

    def get_sendEmail_info(self):
        sendEmail_dict = dict()
        sendEmail_dict['mail_account'] = self.cof.get('sendEmail', 'mail_account')
        sendEmail_dict['mail_pwd'] = self.cof.get('sendEmail', 'mail_pwd')
        sendEmail_dict['mail_sender'] = self.cof.get('sendEmail', 'mail_sender')
        sendEmail_dict['mail_receiver'] = self.cof.get('sendEmail', 'mail_receiver')
        sendEmail_dict['mail_host'] = self.cof.get('sendEmail', 'mail_host')
        sendEmail_dict['mail_port'] = self.cof.get('sendEmail', 'mail_port')
        return sendEmail_dict
    
    """data.ini文件写入/修改操作"""
    def write_data(self, section, key, value):
        self.cof.set(section, key, value)
        self.cof.write(open(final_path, "w"))

    """读取data.ini文件的数据"""
    def get_data(self, section, key):
        data = self.cof.get(section, key)
        return data


if __name__ == '__main__':
    data = ReadData()
    api_info = data.get_api_info()
    sendEmail_info = data.get_sendEmail_info()
    print(api_info, sendEmail_info)



