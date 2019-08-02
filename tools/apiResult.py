import requests
import json
from tools.readCfg import ReadCfg


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'Content-Type': 'application/json'}
Authorization_value = ReadCfg().get_api_info()['Authorization']
headers['Authorization'] = Authorization_value


class ApiResult(object):

    def __init__(self, api_url, api_method, api_data):
        self.headers = headers
        self.method = api_method
        self.url = api_url
        self.data = api_data

    def get_code(self):

        if self.method == 'get':
            api_response = requests.get(headers=self.headers, url=self.url, params=self.data)
            status_code = api_response.status_code
            if api_response.text != '':
                res = api_response.json()
            else:
                res = 0
            return status_code, res

        elif self.method == 'post':
            api_response = requests.post(headers=self.headers, url=self.url, data=self.data)
            status_code = api_response.status_code
            if api_response.text != '':
                res = api_response.json()
            else:
                res = 0
            return status_code, res

        elif self.method == 'put':
            api_response = requests.put(headers=self.headers, url=self.url, data=self.data)
            status_code = api_response.status_code
            if api_response.text != '':
                res = api_response.json()
            else:
                res = 0
            return status_code, res

        else:  # delete请求没有返回值，只有状态码
            api_response = requests.delete(headers=self.headers, url=self.url)
            status_code = api_response.status_code
            if api_response.text != '':
                res = api_response.json()
            else:
                res = 0
            return status_code, res


if __name__ == "__main__":
    url = 'https://www.xxxxxxx.cn/v1/gym/login'
    method = 'post'
    data = {'account_id': 'test01', 'password': 'test01'}
    response = ApiResult(url, method, data)
    code, result = response.get_code()

