#设置代理

import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
import logging

class RandomProxyMiddleware(object):

    #从settings里面获取代理
    def __init__(self,settings):
        self.proxies=settings.getlist('PROXIES')


    def random_paoxy(self):
        return random.choice(self.proxies)

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool(''): #表示事情存在就返回True
            raise NotConfigured(' is False')

        if not crawler.settings.getlist(''):  #自己设置的变量
            raise NotConfigured(' is empty')

        return cls(crawler.settings)

    logger=logging.getLogger(__name__)  #标准的logger文件

    def process_request(self,request,spider):
        if 'proxy' not in request.meta:
            self.logger.debug('Using Proxy')
            request.meta['proxy']=self.random_paoxy()  #这里就添加使用了代理

    #利用process_response重写返回的状态码
    def process_response(self,request,response,spider):
        response.status=201
        return response

    #写之前最好将前面的注释，可能会有点影响
    def process_exception(self,request,exception,spider):
        self.logger.debug('Get Exception')
        return request

