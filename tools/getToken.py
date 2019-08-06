# coding = utf-8
from tools.readCfg import ReadData
from tools.readMysql import ReadMysql
import requests
import json


class GetToken(object):

    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
        self.base_url = ReadData().get_api_info()['base_url']
        self.loginname = ReadData().get_api_info()['loginname']
        self.code = ReadData().get_api_info()['code']
        self.authorization = ReadData().get_api_info()['authorization']
        self.data = {
            "loginname": self.loginname,
            "messageCode": self.code,
            "deviceType": 1
        }
        self.data1 = {
            'id': 1135580521435267073
        }

    def login(self):
        url = self.base_url + '/user/login/loginApp'
        response = requests.post(headers=self.header, url=url, data=self.data)
        res = response.json()
        print(res)
        token = res.get('result')['token']
        final_token = str(token)
        ReadData().write_data('api', 'authorization', final_token)
        return final_token


if __name__ == '__main__':
    obj = GetToken()
    token = obj.login()
    print(token)
    # res = obj.app1()
    # print(res)
    # obj.change_gym()


