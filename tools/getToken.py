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
            'loginname': self.loginname,
            'messageCode': self.code,
            'deviceType': 1
        }
        self.data1 = {
            'id': 1135580521435267073
        }

    def login(self):
        url = self.base_url + '/user/login/loginApp'
        response = requests.post(headers=self.header, url=url, data=self.data1)
        res = response.json()
        token = res.get('result')['token']
        final_token = str(token)
        ReadData().write_data('api', 'authorization', final_token)
        return final_token

    def app1(self):
        header = {
            'user-agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': self.authorization
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=header, url=url, data=self.data1)
        res = response.json()
        print(res)
        return res
    # def change_gym(self):
    #     gym_sql = 'select login_gym_id from account where account_id = "%s"' % self.account
    #     gym_id = ReadMysql().get_data(gym_sql)
    #     url = self.base_url + '/v1/gym/auth/change_gym/' + str(gym_id) + '&api_token = ' + self.login()[7:]
    #     requests.post(headers=self.header, url=url, sql=json.dumps(self.sql))


if __name__ == '__main__':
    obj = GetToken()
    # token = obj.login()
    res = obj.app1()
    print(res)
    # obj.change_gym()


