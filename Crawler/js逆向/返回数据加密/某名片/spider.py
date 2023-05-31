"""
目标网址：https://www.qimingpian.com/innovate
名称：企名片
爬虫类型：js逆向-数据加密
"""
from sqlalchemy import create_engine
import pandas as pd
import time
import requests
import execjs
import json


class InsertMysql:

    def __init__(self, host, user, password, database):
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}", max_overflow=5)

    def insert_mysql(self, table, data):
        return data.to_sql(table, con=self.engine, if_exists='append', index=False)


class Spider(InsertMysql):

    def __init__(self, host, user, password, database, table):
        super().__init__(host, user, password, database)
        self.table = table
        self.url = r'https://vipapi.qimingpian.cn/search/recommendedItemList'
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'vipapi.qimingpian.cn',
            'Origin': 'https://www.qimingpian.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        self.ctx = execjs.compile(
            (open(r'decrypt.js', encoding='utf-8')).read())

    def _post_emit(self, data: dict, current_page: int, retry_times: int, wait: int) -> str:
        """
        post请求，获取页面表单数据
        """
        html_content = None
        i = 0
        while True:
            resp = requests.post(url=self.url, headers=self.header, data=data)
            '''
            if 'Content-Length' in resp.request.headers:
                logging.info(resp.request.headers['Content-Length'])
            '''
            if resp.status_code == 200:
                html_content = resp.text
                print(f'当前第{current_page}页，页面获取成功，重新获取次数{i}次')
                break
            i = i + 1
            if i >= retry_times:
                print(f'当前第{current_page}页，页面获取失败，重新获取次数{i}次')
                break
            else:
                time.sleep(wait)  # try again
        return html_content

    def decrypt(self, data):
        encrypt_data = json.loads(data)
        json_data = self.ctx.call('s', encrypt_data['encrypt_data'])
        list_data = json_data['list']
        df = pd.json_normalize(list_data)
        try:
            df.drop(columns=['hangye2', 'miaoshu', 'yewu'], inplace=True)  # 剔除内容为空或过长
        except KeyError:
            pass

        return df

    def spider(self, current_page: int, max_page: int, retry_times: int, wait: int):
        """
        爬取
        :param current_page: 当前爬取的页面
        :param max_page: 爬取页面总数
        :param retry_times: 爬取失败后重新爬取当前页面的最大次数
        :param wait: 爬取失败后再次爬取的时间间隔
        :return:
        """
        fail_page = []
        while True:

            data = {
                'page': current_page,
                'num': 20,
                'sys': 'vip',
                'keywords': '',
                'unionid': '',
            }

            post_content = self._post_emit(data, current_page, retry_times, wait)
            if post_content is None:
                fail_page.append(current_page)
            else:
                df = self.decrypt(post_content)
                df.to_csv(f'./page_data/page{current_page}'+'.txt', index=False, sep='|')
                self.insert_mysql(self.table, df)
            current_page += 1

            if current_page > max_page:
                break

        return fail_page
