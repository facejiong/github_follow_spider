# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubFollowSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProfileItem(scrapy.Item):
    username = scrapy.Field()
    repositories_counter = scrapy.Field()
    star_counter = scrapy.Field()
    followers_counter = scrapy.Field()
    following_counter = scrapy.Field()
    avatar = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass