import requests
import sql
import time
import db
import logging

from multiprocessing import Pool


class tt_proxy(object):
    def __init__(self):
        self.test_url = db.test_url
        self.headers = db.headers
        self.db_obj = sql.connect_db()

    def req_proxy(self,ip):
        try:
            response = requests.get(self.test_url,headers=self.headers,proxies=ip)
            return response.status_code
        except Exception:
                logging.warning('Faild_proxy IP:%s'%ip['http'])
                self.db_obj.del_ip(ip['http'])
                return ip['http']

    def get_data(self,proxy_all):
        for ip in proxy_all:
            yield {
                'http':ip.decode('utf-8'),
                'https':ip.decode('utf-8')
            }
def main(ip):
    test_cls = tt_proxy()
    test_cls.req_proxy(ip)


def Engine():
    test_cls = tt_proxy()
    while True:
        proxy_all = test_cls.db_obj.all_ip
        # p = Pool()
        # p.map(main, [ip for ip in test_cls.get_data(proxy_all)])
        for ip in test_cls.get_data(proxy_all):
            main(ip)
        print('ok')
        time.sleep(db.times)

if __name__ == '__main__':
    Engine()
