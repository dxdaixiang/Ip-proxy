# _*_ coding:utf-8_*_
import requests
import asyncio
import aiohttp
from concurrent.futures import TimeoutError
import logging
from bs4 import BeautifulSoup
from urllib import parse
import sql
import db
from multiprocessing import Process

db_obj = sql.connect_db()
class get_cls(object):

    def __init__(self):
        self.test_url = db.test_url
        self.req_count = 0
        self.headers = db.headers
    # headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    # }





    async def get_ip(self,url,proxy_url):
        # proxy_url = 'http://127.0.0.1:10800'
        try:
            async with aiohttp.ClientSession() as session:

                if proxy_url:
                    async with session.get(url,headers=self.headers,proxy=proxy_url,timeout=5) as r:
                        if r and r.status:
                            return await r.text(),r.status
                else:
                    async with session.get(url, headers=self.headers) as r:
                        if r and r.status:
                            return await r.text(),r.status

        except Exception:
            self.req_count += 1
            logging.error('%s:::%s:::%s'%(proxy_url,url,self.req_count))
            get_proxy = db_obj.get_proxy
            if get_proxy:
                return await self.get_ip(url,db_obj.get_proxy[0].decode('utf-8'))
            else:
                return await self.get_ip(url)


    async def auth_ip(self,db_obj,ip,contents):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.test_url,proxy=ip,timeout=5) as f:
                    if f and f.status == 200:
                        db_obj.insert(ip)
                        print(contents)
        except Exception:
            logging.warning(ip)
        return None




get_page = get_cls()
async def parse_page(url,proxy_url=None):
    html,req_status = await get_page.get_ip(url,proxy_url)
    if len(html) > 100 and req_status == 200:
        soup = BeautifulSoup(html,'lxml')

        data = soup.select('table#ip_list tr')
        for i in data:
            a = i.select('td')
            if a:
                data = a[5].string.lower() + r'://' + a[1].string + ':' + a[2].string

                try:
                    contents = a[1].string + ':' + a[2].string + '\t' + a[3].select('a')[0].string +'\t' + a[5].string
                except Exception:
                    contents = a[1].string + ':' + a[2].string + '\t' + '' +'\t' + a[5].string
                await get_page.auth_ip(db_obj,data,contents)

        page_num = soup.select('div.pagination a.next_page')
        if page_num and db_obj.get_proxy:
            print(url)
            await parse_page(parse.urljoin(url, page_num[0].attrs['href']),db_obj.get_proxy[0].decode('utf-8'))
        elif page_num and not db_obj.get_proxy:
            print(url)
            await parse_page(parse.urljoin(url, page_num[0].attrs['href']))

    else:
        print(str(req_status) + '--' + url)
        await parse_page(url, db_obj.get_proxy[0].decode('utf-8'))




async def parse_page_2(url,page_num=1,proxy_url=None):
    html,req_status = await get_page.get_ip(url,proxy_url)
    if len(html) > 100 and req_status == 200:
        page_num += 1
        soup = BeautifulSoup(html,'lxml')
        result = soup.select('tbody tr')
        if result:
            for i in result:
                try:
                    data = i.select('td')[3].string.lower().strip() + r'://' + i.select('td')[0].string.strip() + ':' + i.select('td')[1].string.strip()
                    contents = i.select('td')[3].string.lower() + r'://' + i.select('td')[0].string + ':' + i.select('td')[1].string + '\t' + i.select('td')[4].string
                    await get_page.auth_ip(db_obj,data,contents)

                except Exception:
                    logging.warning(url)

            if db_obj.get_proxy:
                print(url)
                await parse_page_2(parse.urljoin(url,str(page_num)),page_num,db_obj.get_proxy[0].decode('utf-8'))
            else:
                print(url)
                await parse_page_2(parse.urljoin(url, str(page_num)), page_num)
    else:
        print(str(req_status)+'--'+url)
        await parse_page_2(url,page_num,db_obj.get_proxy[0].decode('utf-8'))







def main(url_1):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_page(url_1))
    loop.close()

def main_2(url_2):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_page_2(url_2))
    loop.close()



def start_main():
    url_1 = 'http://www.xicidaili.com/nn/'
    url_2 = 'http://www.kuaidaili.com/free/inha/'
    p2 = Process(target=main_2,args=(url_2,))
    p1 = Process(target=main,args=(url_1,))
    p2.start()
    p1.start()
    p2.join()
    p1.join()



if __name__ == '__main__':
    start_main()


