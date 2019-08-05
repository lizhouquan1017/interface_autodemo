import unittest
import requests
import json
from tools.readCfg import ReadData


class SaleOrderController(unittest.TestCase):
    """销售单模块"""

    # 每运行一个用例，初始化一次，避免数据污染（修改全部变量）
    def setUp(self):
        self.authorization = ReadData().get_api_info()['authorization']
        self.base_url = ReadData().get_api_info()['base_url']
        self.header = {
            'user-agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': self.authorization
        }

    def test_00101_submitsaleorder(self):
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
            "channel":  "1",
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

    def test_00201_cancelledSaleOrder(self):
        """销售单挂单接口"""
        data1 = [{
            "goodsCostPrice": 30,
            "goodsDiscount": 10,
            "goodsDiscountMoney": 120,
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
            "orderRetailMoney": 0,
            "orderDetailTransactionMoney": 0,
            "orderTransactionMoney": 120.0,
            "orderDiscountMoney": 0.0,
            "orderDiscount": 10.0,
            "orderPreferentialType": 0,
            "transTypeId": "T101"
        }
        url = self.base_url + '/order/saleOrder/cancelledSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        order_num = res['result']['orderCode']
        order_id = res['result']['id']
        ReadData().write_data('huang_up_order', 'id', order_id)
        ReadData().write_data('huang_up_order', 'ordernum', order_num)
        self.assertEqual(responsecode, 200, '发送请求失败')

    def test_00301_querycancelledsaleorderbyid(self):
        """销售挂单列表销售单详情查询（正常）"""
        huang_up_id = ReadData().get_data('huang_up_order', 'id')
        data = {
            "id": huang_up_id
        }
        url = self.base_url + '/order/saleOrder/queryCancelledSaleOrderById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00302_querycancelledsaleorderbyid(self):
        """销售挂单列表销售单详情查询（id为空）"""
        data = {
            "id": None
        }
        url = self.base_url + '/order/saleOrder/queryCancelledSaleOrderById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        responsemsg = res['responseMsg']
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')
        self.assertEqual(responsemsg, '销售挂单id不能为空', '发送请求失败')

    def test_00401_batchcleancancelledsaleorder(self):
        """批量清空销售单挂单接口（正常）"""
        huang_up_id = ReadData().get_data('huang_up_order', 'id')
        data = {
            "ids": huang_up_id
        }
        url = self.base_url + '/order/saleOrder/batchCleanCancelledSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00402_batchcleancancelledsaleorder(self):
        """批量清空销售单挂单接口（销售单不存在）"""
        data = {
            "ids": 123456
        }
        url = self.base_url + '/order/saleOrder/batchCleanCancelledSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        responsemsg = res['responseMsg']
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')
        self.assertEqual(responsemsg, '批量清空失败!')

    def test_00403_batchcleancancelledsaleorder(self):
        """批量清空销售单挂单接口（销售单id为空）"""
        data = {
            "ids": None
        }
        url = self.base_url + '/order/saleOrder/batchCleanCancelledSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        responsemsg = res['responseMsg']
        self.assertEqual(responsecode, 406, '发送请求失败')
        self.assertEqual(responsemsg, '订单号不能为空', '发送请求失败')
        self.assertEqual(success, False)

    def test_00501_querysaleorderinfobyid(self):
        """销售单详情查询接口（正常）"""
        sale_id = ReadData().get_data('sales_order', 'id')
        data = {
            "id": sale_id  # 销售单id
        }
        url = self.base_url + '/order/saleOrder/querySaleOrderInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True)
        self.assertNotEqual(result, None, '查询失败，返回结果错误')

    def test_00502_querysaleorderinfobyid(self):
        """销售单详情查询接口（查询id不存在）"""
        data = {
            "id": 123456789  # 销售单id
        }
        url = self.base_url + '/order/saleOrder/querySaleOrderInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True)
        self.assertEqual(result, None, '查询失败，返回结果错误')

    def test_00503_querysaleorderinfobyid(self):
        """销售单详情查询接口（id为空）"""
        data = {
            "id": None
        }
        url = self.base_url + '/order/saleOrder/querySaleOrderInfoById'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responscode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responscode, 406, '发送请求失败')
        self.assertEqual(success, False)

    def test_00601_cancelsaleorder(self):
        """销售单作废接口（正常）"""
        sale_id = ReadData().get_data('sales_order', 'id')
        data = {
            "id": sale_id
        }
        url = self.base_url + '/order/saleOrder/cancelSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        self.assertEqual(responsecode, 200, '发送请求失败')
        self.assertEqual(success, True, '发送请求失败')

    def test_00602_cancelsaleorder(self):
        """销售单作废接口（已作废订单重复作废）"""
        sale_id = ReadData().get_data('sales_order', 'id')
        data = {
            "id": sale_id
        }
        url = self.base_url + '/order/saleOrder/cancelSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responsecode = int(res['responseCode'])
        success = res['success']
        responsemsg = res['responseMsg']
        self.assertEqual(responsecode, 1001, '发送请求失败')
        self.assertEqual(responsemsg, '当前订单已作废,不可重复作废', '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')

    def test_00603_cancelsaleorder(self):
        """销售单作废接口（id为空）"""
        data = {
            "id": None
        }
        url = self.base_url + '/order/saleOrder/cancelSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 500, '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')
        self.assertEqual(result, None)

    # 存在问题
    def test_00604_cancelsaleorder(self):
        """销售单作废接口（id错误时）"""
        data = {
            "id": None
        }
        url = self.base_url + '/order/saleOrder/cancelSaleOrder'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        print(res)
        responsecode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responsecode, 500, '发送请求失败')
        self.assertEqual(success, False, '发送请求失败')
        self.assertEqual(result, None)

    def test_00701_cancelpurchasereturnorder(self):
        """销售列表查询接口"""
        data = {
            "pageSize": 15,
            "pageNum": 1,
            "status": 0
        }
        url = self.base_url + '/order/saleOrder/querySaleOrderList'
        response = requests.post(headers=self.header, url=url, data=data)
        res = response.json()
        responseCode = int(res['responseCode'])
        success = res['success']
        result = res['result']
        self.assertEqual(responseCode, 200, '发送请求失败')
        self.assertNotEqual(result, None)
        self.assertEqual(success, True, '发送请求失败')

    def tearDown(self):
        pass


if __name__ == "__main__":

    unittest.main()
