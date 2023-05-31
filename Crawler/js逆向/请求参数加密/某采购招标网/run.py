from Crawler import *

if __name__ == '__main__':
    spider = Crawler()
    # print(f'qt: {spider.qt}\ncookie: {spider.cookie}')

    first_page, max_page = spider.first_page_content(5, 5)
    first_page_data = func.parse_content(first_page)

    # total_data = spider.spider(1, 5, 5, 5) # 自定义，从1到自定义页数
    total_data, fail_list = spider.spider(2, 20, 10, 5)  # 从2到页面最大页数

    total_data = pd.concat([first_page_data, total_data], ignore_index=True)
    print(f'已获取数据记录{total_data.shape[0]}条！')
    total_data.to_excel('页面表单数据.xlsx', index=False)

    if len(fail_list) >= 1:
        fail_title = fail_list.join('、')
        print(f'失败的页面：{fail_title}')

    print('已爬取完毕！')

    """
    因为设置了请求次数上限，会有页面请求失败的情况，fail_list里面存放了失败的页数，若需要可使用下面的语句再次请求
    """
    # fail_page_data = pd.DataFrame()
    # if len(fail_list) >= 1:
    #     for page in fail_list:
    #         data, _ = spider.spider(page, page, 10, 5)
    #         fail_page_data = pd.concat([first_page_data, data], ignore_index=True)
    # fail_page_data.to_excel('失败页面表单数据.xlsx', index=False)