import scrapy
import urllib

from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from github_follow_spider.items import ProfileItem
from github_follow_spider.items import ImageItem

class ProfileSpider(scrapy.Spider):
    name = "profile_spider"
    allowed_domains = ["github.com"]
    start_url = "https://github.com/facejiong"
    download_delay = 1

    def __init__(self, *args, **kwargs):
        super(ProfileSpider, self).__init__(*args, **kwargs)
        self.profile_number = 0
    
    def start_requests(self):
        """
        登陆页面 获取cookie
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
            'https://github.com/facejiong?tab=followers&page=1',
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_followers,
        )]

    def parse_followers(self, response):
        if self.profile_number >= 6000:
            print('profile_number-----------:')
            raise CloseSpider('profile number satisfy close')

        url_params_parse = urllib.parse.urlparse(response.url)
        url_params_dict = urllib.parse.parse_qs(url_params_parse.query)

        page = int(url_params_dict['page'][0], base=10)

        selector = Selector(response)

        # 保存信息
        if (page == 1):
            username = selector.xpath(
                '//span[@class="p-nickname vcard-username d-block"]/text()'
            ).extract()[0]
            counters = selector.xpath(
                '//span[@class="Counter"]/text()'
            ).extract()
            avatar = selector.xpath(
                '//img[@class="avatar width-full rounded-2"]/@src'
            ).extract()
            repositories_counter = counters[0].strip()
            star_counter = counters[1].strip()
            followers_counter = counters[2].strip()
            following_counter = counters[3].strip()
            # print('counters:', counters)
            # print('repositories_counter:', repositories_counter)
            # print('star_counter:', star_counter)
            # print('followers_counter:', followers_counter)
            # print('following_counter:', following_counter)

            # item提取要存储的数据
            item = ProfileItem()
            item['username'] = username
            item['repositories_counter'] = repositories_counter
            item['star_counter'] = star_counter
            item['followers_counter'] = followers_counter
            item['following_counter'] = following_counter
            item['avatar'] = avatar[0]
            yield item

            image_item = ImageItem()
            image_item['image_urls'] = avatar
            self.profile_number += 1
            print('profile_number:', self.profile_number)
            yield image_item

        # followers翻页
        next_page_exist = selector.xpath(
            '//div[@class="pagination"]/a'
        ).re(r'Next')
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
                callback=self.parse_followers,
            )

        # followers列表请求
        followers_urls = selector.xpath(
            '//div[@class="d-table col-12 width-full py-4 border-bottom border-gray-light"]/div[@class="d-table-cell col-9 v-align-top pr-3"]/a[@class="d-inline-block no-underline mb-1"]/@href'
        ).extract()
        for followers_url in followers_urls:
            complete_url = 'https://{}{}{}'.format(self.allowed_domains[0], followers_url, '?tab=followers&page=1')
            # print('complete_url:.......', complete_url)
            yield Request(complete_url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_followers)