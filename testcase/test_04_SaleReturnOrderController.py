import unittest
import requests
import json
from tools.readCfg import ReadData


class PurchaseReturnOrderController(unittest.TestCase):
    """销售退货单模块"""

    # 每运行一个用例，初始化一次，避免数据污染（修改全部变量）
    def setUp(self):
        self.authorization = ReadData().get_api_info()['authorization']
        self.base_url = ReadData().get_api_info()['base_url']
        self.header = {
            'user-agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': self.authorization
        }

    def test_00100_submitsaleorder(self):
        """销售单提交接口（正常）"""
        data1 = [{
            "goodsCostPrice": 30,
            "goodsDiscount": 10,
            "goodsDiscountMoney": 0,
            "goodsPreferentialType": 0,
            "goodsRetailPrice": 120,
            "goodsSkuCode": "1560751503346043",
            "goodsSpuCode": "1560751502987925",
            "goodsTransactionPrice": 120,
            "transQty": 1
        }]
        data2 = [{
            "salesmanId": "1102522113031491586",
            "salesmanName": "老板"
        }]
        data = {
            "accountId": "1102522438563991554",
            "accountName": "现金",
            "channel": "1",
            "orderDetailModel": [json.dumps(data1)],
            "salesmen": [json.dumps(data2)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "remarks": "",
            "supplierName": "供应商1",
            "orderEraseMoney": 0.0,
            "orderRetailMoney": 120.0,
            "orderDetailTransactionMoney": 120.0,
            "orderTransactionMoney": 120.0,
            "orderDiscountMoney": 0.0,
            "orderDiscount": 10.0,
            "orderPreferentialType": 0,
            "transTypeId": "T101"
        }
        url = self.base_url + '/order/saleOrder/submitSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        sale_order_num = res['result']['orderCode']
        sale_order_id = res['result']['id']
        ReadData().write_data('sales_order', 'id', sale_order_id)
        ReadData().write_data('sales_order', 'ordernum', sale_order_num)
        result = res['result']
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200)
        self.assertEqual(success, True)
        self.assertNotEqual(result, None)

    def test_00101_submitsalereturnorder(self):
        """销售退货单提交接口（原单退货正常）"""
        self.test_00100_submitsaleorder()
        sale_id = ReadData().get_data('sales_order', 'id')
        data1 = [{
            "goodsCostPrice": 30,
            "goodsSkuCode": "1560751503346043",
            "goodsSpuCode": "1560751502987925",
            "goodsTransactionPrice": 120,
            "transQty": 1
        }]
        data = {
            "orderOriginId": sale_id,
            "accountId": "1102522438563991554",
            "accountName": "现金",
            "channel":  "1",
            "orderDetailModel": [json.dumps(data1)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "orderTransactionMoney": 120,
            "remarks": "",
            "transTypeId": "T103"
        }
        url = self.base_url + '/order/saleReturnOrder/submitSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = res['result']
        sale_return_order_num = res['result']['orderCode']
        sale_return_order_id = res['result']['id']
        ReadData().write_data('sales_return_order', 'id', sale_return_order_id)
        ReadData().write_data('sales_return_order', 'ordernum', sale_return_order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')

    def test_00102_submitpurchasereturnorder(self):
        """销售退货单提交接口（直接退货正常）"""
        data1 = [{
            "goodsCostPrice": 30,
            "goodsSkuCode": "1560751503346043",
            "goodsSpuCode": "1560751502987925",
            "goodsTransactionPrice": 120,
            "transQty": 1
        }]
        data2 = [{
            "salesmanId": "1102522113031491586",
            "salesmanName": "老板"
        }]
        data = {
            "accountId": "1102522438563991554",
            "accountName": "现金",
            "channel":  "1",
            "orderDetailModel": [json.dumps(data1)],
            "orderSkuQty": "1",
            "orderSpuQty": "1",
            "orderTransactionMoney": 120,
            "remarks": "",
            "transTypeId": "T102",
            "salesmen": [json.dumps(data2)]
        }
        url = self.base_url + '/order/saleReturnOrder/submitSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = int(res['success'])
        result = res['result']
        sale_order_num = res['result']['orderCode']
        sale_order_id = res['result']['id']
        ReadData().write_data('sales_return_order', 'id', sale_order_id)
        ReadData().write_data('sales_return_order', 'ordernum', sale_order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')

    def test_00201_cancelsalereturnorde(self):
        """作废销售退货单接口（正常）"""
        sale_return_id = ReadData().get_data('sales_return_order', 'id')
        data = {
            "id": sale_return_id  # 销售退货单id
        }
        url = self.base_url + '/order/saleReturnOrder/cancelSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00202_cancelpurchasereturnorder(self):
        """作废销售退货单接口（已作废订单id）"""
        sale_return_id = ReadData().get_data('sales_return_order', 'id')
        data = {
            "id": sale_return_id  # 采购订单id
        }
        url = self.base_url + '/order/saleReturnOrder/cancelSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(responsemsg, '销售退货单已作废!', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00203_cancelpurchasereturnorder(self):
        """作废销售退货单接口（销售退货单id为空）"""
        data = {
            "id": None  # 销售退货单id
        }
        url = self.base_url + '/order/saleReturnOrder/cancelSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '销售退货单id不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    # 有争议问题
    def test_00204_cancelpurchaseorder(self):
        """作废销售单退货接口（销售退货单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + '/order/saleReturnOrder/cancelSaleReturnOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        success = res['success']
        self.assertEqual(success, False, '发送请求失败')

    def test_00301_querypurchasereturnInfo(self):
        """销售退货单详情查询接口（正常）"""
        sale_id = ReadData().get_data('sales_return_order', 'id')
        data = {
            "id": sale_id  # 采购订单id
        }
        url = self.base_url + '/order/saleReturnOrder/querySaleReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertNotEqual(result, None, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00302_querypurchasereturnInfo(self):
        """销售退货单详情查询接口（销售退货单id错误）"""
        data = {
            "id": 1234567890  # 采购订单id
        }
        url = self.base_url + '/order/saleReturnOrder/querySaleReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')
        self.assertEqual(result, None, '发送请求失败')

    def test_00303_querypurchasereturnInfo(self):
        """销售退货单详情查询接口（销售退货单id为空）"""
        data = {
            "id": None  # 采购订单id
        }
        url = self.base_url + '/order/saleReturnOrder/querySaleReturnInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        responsemsg = res['responseMsg']
        success = res['success']
        print(res)
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '销售单退货单号不能为空', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00401_querypurchasereturnorderList(self):
        """销售退货单列表查询接口（正常）"""
        data = {
            "pageSize": 15,
            "pageNum": 1,
            "status": 0
        }
        url = self.base_url + '/order/saleReturnOrder/querySaleReturnOrderList'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
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
