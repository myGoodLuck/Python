# -*- coding: utf-8 -*-
import scrapy
class NewyorkerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title =scrapy.Field()
    article_url = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    article =scrapy.Field()
    image_urls =scrapy.Field()
    w_sum=scrapy.Field()
    v_sum=scrapy.Field()
    s_sum=scrapy.Field()
    p_sum=scrapy.Field()
    a_sum=scrapy.Field()
    avg_s=scrapy.Field()
    avg_w=scrapy.Field()
    avg_p=scrapy.Field()

    pass
