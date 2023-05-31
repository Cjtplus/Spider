import random
import time
import requests
import func
import pandas as pd
from config import *
from pyquery import PyQuery as pq


class Crawler:
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    user_agent = random.choice(User_Agent)
    login_headers['User-Agent'] = user_agent
    post_headers['User-agent'] = user_agent

    def __init__(self):
        self.login_url = login_url
        self.post_url = post_url
        self.login_header = login_headers
        self.post_header = post_headers

        self.session = requests.session()
        self.cookie, self.qt = self.login(self.login_url, self.login_header)

        self.post_header['cookie'] = self.cookie

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
        page_data = pd.DataFrame()
        while True:

            data = self.generate_data(current_page)
            post_content = self.post_emit(self.post_url, self.post_header, data, current_page, retry_times, wait)
            if post_content is None:
                fail_page.append(current_page)
            else:
                df = func.parse_content(post_content)
                page_data = pd.concat([page_data, df], ignore_index=True)
            current_page += 1

            if current_page > max_page:
                break

        return page_data, fail_page

    def login(self, url: str, headers: dict):
        """
        获取请求表单数据的cookie和qt
        :param url:请求的初始链接
        :param headers:请求的初始表头
        :return:
        """
        cookie = ''
        qt = ''
        ret = self.session.get(url=url, headers=headers)
        status_code = ret.status_code
        if status_code == 200:
            items = ret.cookies.items()
            info = ''
            for name, value in items:
                info += '{0}={1};'.format(name, value)
            cookie = info
            qt = func.parser_qt(ret.text)
        return cookie, qt

    def generate_data(self, current_page: int) -> dict:
        """
        构成post请求的表单数据
        :param current_page: 当前页数
        :return:
        """
        data = {
            'page.currentPage': str(current_page),
            'page.perPageSize': '20',
            'noticeBean.sourceCH': '',
            'noticeBean.source': '',
            'noticeBean.title': '',
            'noticeBean.startDate': '',
            'noticeBean.endDate': '',
            '_qt': self.qt
        }

        return data

    def post_emit(self, url: str, headers: dict, data: dict, current_page: int, retry_times: int, wait: int) -> str:
        """
        post请求，获取页面表单数据
        """
        html_content = None
        i = 0
        while True:
            resp = self.session.post(url=url, headers=headers, data=data)
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

    def first_page_content(self, retry_times: int, wait: int):
        """
        获取第一页，返回第一页页面html，最大页数
        """
        data = self.generate_data(1)
        content = self.post_emit(self.post_url, self.post_header, data, 1, retry_times, wait)

        while content is None:
            content = self.post_emit(self.post_url, self.post_header, data, 1, retry_times, wait)

        content = pq(content)
        page_div = content('td#pageid2')
        page_td = page_div('span')

        total_page = ''
        for item in page_td.items():
            # print(item.text())
            if '条数据' in item.text():
                total_page = eval(item.text().split('/')[1][:-1].replace(',', ''))

        return content, total_page


# if __name__ == '__main__':
#     spider = Crawler()
#     print(f'qt: {spider.qt}\ncookie: {spider.cookie}')
#
#     first_page, max_page = spider.first_page_content(5, 5)
#     first_page_data = func.parse_content(first_page)
#
#     # total_data = spider.spider(1, 5, 5, 5) # 自定义，从1到自定义页数
#     total_data = spider.spider(2, max_page, 5, 5)  # 从2到页面最大页数
#
#     total_data = pd.concat([first_page_data, total_data], ignore_index=True)
#     print(total_data.shape)
#     total_data.to_excel('页面表单数据.xlsx', index=False)
#     print('已爬取完毕！')
