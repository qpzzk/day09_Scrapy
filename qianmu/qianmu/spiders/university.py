# -*- coding: utf-8 -*-
#普通scrapy

import scrapy
from w3lib.html import remove_tags
from ..items import UniversityItem

def filter(html):
     #过滤网页源码中的特殊符号和sup标签
    return remove_tags(html,which_ones=('sup',)).replace('\n','').replace('\r','').replace    ('\t','')


class UniversitySpider(scrapy.Spider):
    name = 'university'
    allowed_domains = ['140.143.192.76']
    start_urls = ['http://140.143.192.76:8002/2018USNEWS世界大学排名']

    def __init__(self,max_num=0,name=None,**kwargs):
        super(UniversitySpider,self).__init__(name,**kwargs)
        self.max_num = int(max_num)

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url,meta={'download_timeout':10},callback=self.parse)

    def parse(self, response):
        self.logger.info(self.max_num)
        links=response.xpath("//div[@id='content']//tr[position()>1]/td[2]//@href").extract()
        for i,link in enumerate(links):   #enumerate给其加入索引
            if self.max_num and i >= self.max_num:
                break
            if not link.startswith('http://'):
                link='http://140.143.192.76:8002%s' % link
            request=scrapy.Request(link,callback=self.parse_university)
            request.meta['rank']= i + 1
            print(response.status)
            yield request
    
    def parse_university(self,response):
        self.logger.info('%s %s' %('-'*50,response.meta))
        response=response.replace(body=filter(response.text))
        wiki_content=response.xpath('//div[@id="wikiContent"]')
       # item=UniversityItem(name=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').extract_first())
        item=UniversityItem(
            name=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').extract_first(),
            rank=response.meta['rank'],
        )

        keys=wiki_content.xpath('./div[@class="infobox"]/table//tr/td[1]//text()').extract()
        cols=wiki_content.xpath('./div[@class="infobox"]/table//tr/td[2]')
        values=[','.join(col.xpath('.//text()').extract()) for col in cols]
        data=dict(zip(keys,values))
        item['country']=data.get(u'国家','')
        item['state']=data.get(u'州省','')
        item['city']=data.get(u'城市','')
        item['undergraduate_num']=data.get(u'本科人数','')
        item['postgraduate_num']=data.get(u'研究生人数','')
        item['website']=data.get(u'网址','')
        self.logger.info('%s scraped' % item[u'name'])
        yield item


