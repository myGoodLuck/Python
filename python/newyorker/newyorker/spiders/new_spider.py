# -*- coding:utf-8 -*-
import re
import requests
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from bs4 import  BeautifulSoup
from scrapy.selector import Selector
from newyorker.items import NewyorkerItem

class newyorker(CrawlSpider):
    name = "newyorker"
    allowed_domains = ["newyorker.com"]
    start_urls = ['http://www.newyorker.com/news/daily-comment/']


    def parse(self, response):
         sel = Selector(response)
         infos = sel.xpath("//main/div/ul/li")

         for info in infos:
             article_url_part = info.xpath("div/h4/a/@href").extract()[0]
             article_url = 'http://www.newyorker.com/'+article_url_part
             yield Request(article_url,meta={'article_url':article_url},callback=self.parse_item)


         urls = ['http://www.newyorker.com/news/daily-comment/page/{}'.format(str(i)) for i in range(1,10)]
         for url in urls:
                 yield Request(url,callback=self.parse)


    def parse_item(self,response):
        item = NewyorkerItem()

        item['article_url'] = response.meta['article_url']
        data =requests.get(response.meta['article_url'])

        sel =Selector(response)
        title = sel.xpath("//h1/text()").extract()[0]
        author = sel.xpath("//div/div/div[2]/p/a/text()").extract()[0]
        time = sel.xpath("//hgroup/div[2]/p/text()").extract()[0]
       

        soup=BeautifulSoup(data.text,'lxml')
        image_urls = soup.select('figure > div > picture > img')[0].get('srcset')if soup.find_all('picture','component-responsive-image')  else None
        articles=soup.select('#articleBody p')
        article = [i.text +'<br />' for i in articles]
        article_process = str(article).replace("', '"," ").strip("['").strip("']").strip(" ?").replace('\\xa0','')
        w_sum = len(re.findall('[a-zA-Z]+', article_process))
        s_sum = len(re.findall('([.!?].\s?[A-Z����])', article_process))
        p_sum = len(article)
        v_sum = len(set(re.findall('[a-zA-Z]+', article_process.lower())))
        a_sum = len(re.findall('[a-zA-Z]', article_process))
        avg_w = round(a_sum / w_sum, 2)
        avg_s = round(w_sum / s_sum, 2)
        avg_p = round(s_sum / p_sum, 2)

        item['title']=title     #标题
        item['author']=author   #作者
        item['time']=time        #时间
        item['article']=article_process  #正文
        item['image_urls']= image_urls   #图片
        item['w_sum']=w_sum         #单词
        item['s_sum']=s_sum         #句子
        item['p_sum']=p_sum         #段落
        item['v_sum']=v_sum         #词汇
        item['a_sum']=a_sum         #字母
        item['avg_w']=avg_w #平均单词长度
        item['avg_s']=avg_s #平均句子长度
        item['avg_p']=avg_p #平均段落长度
        yield item








