# coding = utf-8

import configparser
from os import path
# from tools.base import BaseView

parent_path = path.dirname(path.dirname(__file__))
final_path = path.join(parent_path, "sql\purchase.ini")


class ReadPurchase(object):

    def __init__(self):
        self.cof = configparser.ConfigParser()
        self.cof.read(final_path, encoding='utf-8')

    def get_purchase_order_id(self):
        sql = self.cof.get('id', 'sql')
        return sql

    def write_data(self, section, key, value):
        self.cof.set(section, key, value)
        self.cof.write(open(final_path, "w"))


if __name__ == '__main__':
    data = ReadPurchase()
    api_info = data.get_purchase_order_id()
    print(api_info)



