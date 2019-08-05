import unittest
import requests
import json
from tools.readCfg import ReadData


class PurchaseReturnOrderController(unittest.TestCase):
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

    def test_00100_submitpurchaseorder(self):
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
        purchase_order_num = res['result']['orderCode']
        purchase_order_id = res['result']['id']
        ReadData().write_data('purchase_order', 'id', purchase_order_id)
        ReadData().write_data('purchase_order', 'ordernum', purchase_order_num)

    def test_00101_submitpurchasereturnorder(self):
        """采购退货单提交接口（原单退货正常）"""
        self.test_00100_submitpurchaseorder()
        purchase_id = ReadData().get_data('purchase_order', 'id')
        data1 = [{
            "goodsCostPrice": 30,
            "goodsSkuCode": "1560751503346043",
            "goodsSpuCode": "1560751502987925",
            "goodsTransactionPrice": 30,
            "transQty": 1
        }]
        data = {
            "orderOriginId": purchase_id,
            "accountId": "1102522438563991554",
            "accountName": "现金",
            "channel":  "1",
            "orderDetailModel": [json.dumps(data1)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "orderTransactionMoney": 30.0,
            "remarks": "",
            "supplierName": "供应商1",
            "supplierId": "1559464679881381",
            "transTypeId": "T203"
        }
        url = self.base_url + '/order/purchaseReturnOrder/submitPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = int(res['result'])
        purchase_return_order_num = res['result']['orderCode']
        purchase_return_order_id = res['result']['id']
        ReadData().write_data('purchase_return_order', 'id', purchase_return_order_id)
        ReadData().write_data('purchase_return_order', 'ordernum', purchase_return_order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')

    def test_00102_submitpurchasereturnorder(self):
        """采购退货单提交接口（直接退货正常）"""
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
            "channel":  "1",
            "orderDetailModel": [json.dumps(data1)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "orderTransactionMoney": 30.0,
            "remarks": "",
            "supplierName": "供应商1",
            "supplierId": "1559464679881381",
            "transTypeId": "T202"
        }
        url = self.base_url + '/order/purchaseReturnOrder/submitPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = int(res['result'])
        purchase_order_num = res['result']['orderCode']
        purchase_order_id = res['result']['id']
        ReadData().write_data('purchase_return_order', 'id', purchase_order_id)
        ReadData().write_data('purchase_return_order', 'ordernum', purchase_order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')

    def test_00201_cancelpurchaseorder(self):
        """作废采购退货单接口（正常）"""
        purchase_return_id = ReadData().get_data('purchase_return_order', 'id')
        data = {
            "id": purchase_return_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/cancelPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00202_cancelpurchasereturnorder(self):
        """作废采购退货单接口（已作废订单id）"""
        purchase_return_id = ReadData().get_data('purchase_return_order', 'id')
        data = {
            "id": purchase_return_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/cancelPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(responsemsg, '采购退货单已作废!', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00203_cancelpurchasereturnorder(self):
        """作废采购退货单接口（采购退货单id为空）"""
        data = {
            "id": None  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/cancelPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '采购退货单号不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    # 有争议问题
    def test_00204_cancelpurchaseorder(self):
        """作废采购单退货接口（采购退货单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + 'order/purchaseReturnOrder/cancelPurchaseReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        success = res['success']
        print(res)
        self.assertEqual(success, False, '发送请求失败')

    def test_00301_querypurchasereturnInfo(self):
        """采购退货单详情查询接口（正常）"""
        purchase_id = ReadData().get_data('purchase_return_order', 'id')
        data = {
            "id": purchase_id  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/queryPurchaseReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = int(res['result'])
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00302_querypurchasereturnInfo(self):
        """采购退货单详情查询接口（采购退货单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/queryPurchaseReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = int(res['result'])
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertEqual(result, None, '发送请求失败')

    def test_00303_querypurchasereturnInfo(self):
        """采购退货单详情查询接口（采购退货单id为空）"""
        data = {
            "id": None  # 采购订单id
        }
        url = self.base_url + '/order/purchaseReturnOrder/queryPurchaseReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        print(res)
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '订单号不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00401_querypurchasereturnorderList(self):
        """采购退货单列表查询接口（正常）"""
        data = {
            "pageSize": 15,
            "pageNum": 1,
            "status": 0
        }
        url = self.base_url + '/order/purchaseReturnOrder/queryPurchaseReturnOrderList'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def tearDown(self):
        pass


if __name__ == "__main__":

    unittest.main()
