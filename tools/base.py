# coding = utf-8

from tools.conn import Database
import logging
import csv

class BaseView(Database):

    # 数据库中查找数据
    def select_data_from_db(self, sql):
        self.connmysql()
        data = self.fetch_all(sql)
        self.close()
        return data

    # 从csv文件中获取数据
    def get_csv_data(self, csv_file, line):
        logging.info(r'获取输入数据')
        with open(csv_file, 'r', encoding='gbk') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader, 1):
                if index == line:
                    return row

    # 存数据导csv文件
    def save_csv_data(self, csv_file, datas):
        logging.info(r'存储数据到%s' % csv_file)
        with open(csv_file, 'w', encoding='gbk') as file:
            file.write(datas+'\n')
            logging.info(r'数据保存成功')

    # 更新数据导csv文件
    def update_csv_data(self, csv_file, index, flag, old, new):
        filereader = open(csv_file, 'r')
        rows = filereader.readlines()
        filewriter = open(csv_file, 'w')
        for line in rows:
            l = line.split(',')
            if l[index] == flag:
                filewriter.writelines(line.replace(old, new))
            else:
                filewriter.writelines(line)
        filewriter.close()
        filereader.close()

