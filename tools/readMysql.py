import pymysql
from database.readPurchase import ReadPurchase


class ReadMysql(object):

    def get_data(self, sql):
        try:
            global cur
            global conn
            conn = pymysql.connect(
                port=3306,
                database='jxc',
                user='jxc',
                passwd='jxc',
                host='10.10.13.120')
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchone()
            if data:
                return data[0]
            else:
                return 0
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()


if __name__ == "__main__":
    # sql = "SELECT * from jxc_t_purchase_order p, jxc_t_user u " \
    #       "where order_code = 'CGRK190602AA001'and u.id = p.create_user and u.phone_num = 15927169432 "
    sql = ReadPurchase().get_purchase_order_id()
    data = ReadMysql().get_data(sql)
    print(data)
