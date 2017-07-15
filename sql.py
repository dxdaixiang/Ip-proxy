# _*_coding:utf-8_*_

import redis
import db

class connect_db(object):
    def __init__(self,sql=None):
        self.host = db.HOST
        self.port = db.PORT
        self.sql = sql
        self.pool = redis.ConnectionPool(host=self.host,port=self.port)
        self.conn = redis.Redis(connection_pool=self.pool)

    def insert(self,ip):
        self.conn.sadd('IP',ip)
        return True

    @property
    def get_proxy(self):
        proxy_ip = self.conn.srandmember('IP',1)
        return proxy_ip

    def del_ip(self,ip=None):
        self.conn.srem('IP',ip)

    @property
    def count_ip(self):
        return self.conn.scard('IP')

    @property
    def all_ip(self):
        return self.conn.smembers('IP')

if __name__ == '__main__':
    db_obj = connect_db()
    # db_obj.insert()
    print(db_obj.get_proxy)
    print(db_obj.count_ip)
    for i in db_obj.all_ip:
        print(i)






# conn.sadd('IP',self.sql)
