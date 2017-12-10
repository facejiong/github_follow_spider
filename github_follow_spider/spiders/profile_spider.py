import scrapy
import urllib.parse

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
            'https://github.com/opengiineer?tab=following&page=1',
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_following,
        )]

    def parse_following(self, response):
        url_params_parse = urllib.parse.urlparse(response.url)
        url_params_dict = urllib.parse.parse_qs(url_params_parse.query)

        page = int(url_params_dict['page'][0], base=10)

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
        next_page_exist = selector.xpath(
            '//div[@class="pagination"]/a'
        ).re(r'Next')

        # following翻页
        if next_page_exist:
            next_page = selector.xpath(
                '//div[@class="pagination"]/a/@href'
            ).extract()
            if page >= 2:
                next_page_url = next_page[1]
            else:
                next_page_url = next_page[0]
            
            yield Request(
                next_page_url,
                meta={'cookiejar': response.meta['cookiejar']},
                callback=self.parse_following,
            )
            print(next_page_url)
            print(next_page)

        # following列表请求
        for following_url in following_urls:
            complete_url = 'https://{}{}{}'.format(self.allowed_domains[0], following_url, '?tab=following&page=1')
            print('complete_url:...', complete_url)
            yield Request(complete_url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_following)
        print(following_urls)
        print(next_page_exist)