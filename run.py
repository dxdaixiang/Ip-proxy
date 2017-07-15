#! /usr/bin/env python3
# _*_coding:utf-8_*_


import master_proxy, auto_proxy,db
from multiprocessing import Process

def main():
    if db.PROXY_VOLUME_CONTROL and db.PROXY_AVAILABLE_CONTROL:
        return 'SUCCESS_ALL'
    else:
        if db.PROXY_VOLUME_CONTROL:
            return 'SUCCESS_VALUME'
        elif db.PROXY_AVAILABLE_CONTROL:
            return 'SUCCESS_AVAILABLE'

if __name__ == '__main__':
    result = main()
    if result == 'SUCCESS_ALL':
        df_val = Process(target=master_proxy.volume)
        df_avai = Process(target=auto_proxy.Engine)
        df_val.start()
        df_avai.start()
        df_val.join()
        df_avai.join()
    elif result == 'SUCCESS_VALUME':
        df_val = Process(target=master_proxy.volume)
        df_val.start()
        df_val.join()
    elif result == 'SUCCESS_AVAILABLE':
        df_avai = Process(target=auto_proxy.Engine)
        df_avai.start()
        df_avai.join()

