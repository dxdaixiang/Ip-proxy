# _*_coding:utf-8_*_

import sql
import db
import time
import get_request

db_obj = sql.connect_db()
def volume():
    if db_obj.count_ip >= db.proxy_pool:
        print(db_obj.count_ip)
        time.sleep(db.times)
        return volume()
    else:
        get_request.start_main()
        return volume()


if __name__ == '__main__':
    volume()






