from spider import *

if __name__ == '__main__':
    spider = Spider(host='xxx', user='xxx', password='xxxx', database='xxx', table='xxx')
    fail_page = spider.spider(current_page=1, max_page=5, retry_times=5, wait=5)
    # 从第一页开始，到第五页， 每次失败后尝试爬取5次， 每次间隔5秒

    length = len(fail_page)
    if length >= 1:
        print(f'{length}页爬取失败')
    else:
        print('爬取完成')
