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

    def test_00101_submitpurchaseorder(self):
        """采购单提交接口（正常）"""
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
        print(res)
        responsecode = int(res['responseCode'])
        purchase_order_num = res['result']['orderCode']
        purchase_order_id = res['result']['id']
        ReadData().write_data('purchase_order', 'id', purchase_order_id)
        ReadData().write_data('purchase_order', 'ordernum', purchase_order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')

    def test_00201_cancelpurchaseorder(self):
        """作废采购单接口（正常）"""
        purchase_id = ReadData().get_data('purchase_order', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success,True)

    def test_00202_cancelpurchaseorder(self):
        """作废采购单接口（已作废订单id）"""
        purchase_id = ReadData().get_data('purchase_order', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(responsemsg, '当前订单已作废,不可重复作废', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00203_cancelpurchaseorder(self):
        """作废采购单接口（采购单id为空）"""
        data = {
            "id": None  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '订单号不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    # 有争议问题
    def test_00204_cancelpurchaseorder(self):
        """作废采购单接口（采购单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/cancelPurchaseOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        print(res)
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00301_querypurchaseInfo(self):
        """采购单详情查询接口（正常）"""
        purchase_id = ReadData().get_data('purchase_order', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        result = res['result']
        success = res['success']
        self.assertNotEqual(result, None)
        self.assertEqual(success, True)
        self.assertEqual(responsecode, 200, '发送请求失败')

    # 有争议问题
    def test_00302_querypurchaseInfo(self):
        """采购单详情查询接口（采购单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        result = res['result']
        success = res['success']
        self.assertEqual(success, True)
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(result, None)

    def test_00303_querypurchaseInfo(self):
        """采购单详情查询接口（采购单id为空）"""
        data = {
            "id": ""  # 采购订单id
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsesode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        result = res['result']
        self.assertEqual(responsesode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '采购单id不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')
        self.assertEqual(result, None)

    def test_00401_querypurchaseorderList(self):
        """采购单列表查询接口（正常）"""
        data = {
            "pageSize": 15,
            "pageNum": 1,
            "status": 0
        }
        url = self.base_url + '/order/purchaseOrder/queryPurchaseOrderList'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True)
        self.assertNotEqual(result, None)

    def tearDown(self):
        pass


if __name__ == "__main__":

    unittest.main()
