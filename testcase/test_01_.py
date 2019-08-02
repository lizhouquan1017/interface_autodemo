import unittest
import requests
import json
from tools.readCfg import ReadData


class PurchaseOrderController(unittest.TestCase):

    """采购单模块"""

    # 每运行一个用例，初始化一次，避免数据污染（修改全部变量）
    def setUp(self):
        self.authorization = ReadData().get_api_info()['authorization']
        self.base_url = ReadData().get_api_info()['base_url']
        self.header = {
            'user-agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': self.authorization
        }

    def test_001_submitpurchaseorder(self):
        """采购单提交接口"""
        data1 = [{
            "goodsCostPrice": 30,
            "goodsSkuCode": "1560751503346043",
            "goodsSpuCode": "1560751502987925",
            "goodsTransactionPrice": 30,
            "transQty": 1
        }]
        data = {
            "accountId": "1102522438563991554",
            "accountName": "现金",
            "channel":  "1",  # 19:IOS 20.Android 21:PC
            "orderDetailModel": [json.dumps(data1)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "orderTransactionMoney": 30.0,
            "remarks": "",
            "supplierName": "供应商1",
            "supplierId": "1559464679881381",
            "transTypeId": "T201"
        }
        url = self.base_url + '/order/purchaseOrder/submitPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responseCode = int(res['responseCode'])
        purchase_order_num = res['result']['orderCode']
        purchase_order_id = res['result']['id']
        ReadData().write_data('purchase', 'id', purchase_order_id)
        ReadData().write_data('purchase', 'ordernum', purchase_order_num)
        self.assertEqual(responseCode, 200, '发送请求失败')

    def test_002_cancelpurchaseorder(self):
        """作废采购单接口"""
        purchase_id = ReadData().get_data('purchase', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responseCode = int(res['responseCode'])
        self.assertEqual(responseCode, 200, '发送请求失败')

    def test_003_querypurchaseInfo(self):
        """采购单查询接口"""
        purchase_id = ReadData().get_data('purchase', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responseCode = int(res['responseCode'])
        self.assertEqual(responseCode, 200, '发送请求失败')

    def test_004_querypurchaseorderList(self):
        """采购单列表查询接口"""
        data = {
            "pageSize": 15,
            "pageNum": 1,
            "status": 0
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseOrderList'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responseCode = int(res['responseCode'])
        self.assertEqual(responseCode, 200, '发送请求失败')

    def tearDown(self):
        pass


if __name__ == "__main__":

    unittest.main()
