import scrapy
from scrapy_dangdang.items import ScrapyDangdangItem


class DangSpider(scrapy.Spider):
    name = 'dang'
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.01.02.00.00.00.html']
    base_url = 'http://category.dangdang.com/pg'
    page = 1

    def parse(self, response):
        li_list = response.xpath('//ul[@id="component_59"]/li')
        for li in li_list:
            # title = li.xpath('.//p[@class="name"]/a/@title').extract_first()
            #  第一张图片和其他的图片的标签是属性是不一样的
            #  第一张图片src是可以使用的 其他图片的地址data-original
            src = li.xpath('.//img/@exam-original').extract_first()
            if src:
                src = src
            else:
                src = li.xpath('.//img/@src').extract_first()

            name = li.xpath('.//img/@alt').extract_first()
            author = li.xpath('.//p[@class="search_book_author"]/span[0]/a[0]/@title').extract_first()
            price = li.xpath('.//p[@class="price"]/span[1]/text()').extract_first()

            # book = ScrapyDangdangItem(title=title, src=src, name=name, author=author, price=price)
            book = ScrapyDangdangItem(src=src, name=name, author=author, price=price)
            # print(book)
            # 获取一个book就交给pipelines
            yield book

        # 每一页爬取的业务逻辑都是一样的
        # 所以我们只需要将执行的那个页的请求再次调用parse方法就可以了
        # if self.page < 10:
        #     self.page = self.page + 1
        #     url = self.base_url + str(self.page) + '-cp01.01.02.00.00.00.html'
        #     # 怎么去调用parse方法
        #     # scrapy.Request就是scrpay的get方法
        #     # url就是请求地址
        #     # callback是你要执行的那个函数 注意不需要加圆括号
        #     yield scrapy.Request(url=url, callback=self.parse)
