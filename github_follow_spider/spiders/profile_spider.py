import scrapy

from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

class QuotesSpider(scrapy.Spider):
    name = "profile_spider"
    allowed_domains = ["github.com"]
    start_url = "https://github.com/facejiong"
    
    def start_requests(self):
        """
        登陆页面 获取xrsf
        """
        return [Request(
            "https://github.com/login",
            meta={'cookiejar': 1},
            callback=self.post_login
        )]

    def post_login(self, response):
        """
        解析登陆页面，发送登陆表单
        """
        return [FormRequest(
            'https://github.com/session',
            method='POST',
            meta={'cookiejar': response.meta['cookiejar']},
            formdata={
                'login': '2279763407@qq.com',
                'password': 'wang1992'},
            callback=self.after_login
        )]

    def after_login(self, response):
        """
        登陆完成后从第一个用户开始爬数据
        """
        return [Request(
            'https://github.com/facejiong?tab=following',
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_following,
        )]

    def parse_following(self, response):
        print(response.url)
        selector = Selector(response)
        username = selector.xpath(
            '//span[@class="p-nickname vcard-username d-block"]/text()'
        ).extract()[0]
        avatar = selector.xpath(
            '//img[@class="avatar width-full rounded-2"]/@src'
        ).extract()[0]
        following_urls = selector.xpath(
            '//div[@class="d-table col-12 width-full py-4 border-bottom border-gray-light"]/div[@class="d-table-cell col-9 v-align-top pr-3"]/a[@class="d-inline-block no-underline mb-1"]/@href'
        ).extract()
        next_page = selector.css('.pagination')
        print(following_urls)
        print(avatar)

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)