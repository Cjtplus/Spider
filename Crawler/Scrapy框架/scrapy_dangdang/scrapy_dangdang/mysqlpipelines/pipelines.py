from scrapy_dangdang.mysqlpipelines.sql import MySql
from scrapy_dangdang.items import ScrapyDangdangItem


class SqlPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, ScrapyDangdangItem):  # 判断item是否存在
            # title = str(item['title'])
            src = str(item['src'])
            name = str(item['name'])
            author = str(item['author'])
            # price = float(str(item['price']).split('¥')[1])
            price = str(item['price']).split('¥')[1]

            # print(type(src))
            # print(type(name))
            # print(type(author))
            # print(type(price))
            # print(title, src, name, author, price, end='\n')
            # 以上获取爬取的数据
            ret = MySql.select(src)  # 判断数据是否存在在数据库中
            print(ret)
            if ret is None:
                # 若数据库中没有数据，保存item
                print('开始保存')
                MySql.insert(src, name, author, price)
            else:
                print('已经存在，等待更新')
                # 若数据库中有以前的数据，更新数据库
                MySql.update(src, name, author, price)
                pass

        else:
            print('no find items')

        return item
