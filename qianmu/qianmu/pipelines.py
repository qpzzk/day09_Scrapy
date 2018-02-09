# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import redis
import logging
import pymysql

logger=logging.getLogger(__name__)   #创建一个logging对象

#item的管道
class CheckPipeline(object):
    def open_spider(self,spider):
        logger.info('spider %s is opened' % spider.name)

    def close_spider(self,spider):
        logger.info('spider %s is closed' % spider.name)

    def process_item(self, item, spider):
        if not item.get('undergraduate_num') and item.get('postgraduate_num'):
            raise DropItem("Missing undergraduate_num or postgraduate_num in %s" % item['name'])
        return item

#设置好redis的缓存管道
class RedisPipeline(object):
    #新建好redis的配置
    def __init__(self):
        self.r=redis.Redis()

    #以item的名字存取
    def process_item(self,item,spider):
        self.r.sadd(spider.name,item['name'])
        logger.info('redis:add %s to list %s' % (item['name'],spider.name))
        return item

#设置mysql的缓存管道
class MysqlPipeline(object):
    def __init__(self):
        self.conn=None
        self.cur=None

    def open_spider(self,spider):
        #当spider启动时，开始使用，连接
        self.conn=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='111111',
            db='qianmu',
            charset='utf8'
        )
        self.cur=self.conn.cursor()   #相当于声明下Mysql的游标

    def process_item(self,item,spider):
        #mysql的插入数据语句
        sql="INSERT INTO `qianmu`.`universities`" \
            " (`name`, `rank`, `country`, `state`, `city`, `undergraduate_num`, `postgraduate_num`, `website`) " \
            "VALUES ("+','.join(['%s']*8)+")"    #copy里面的sql语句
        self.cur.execute(sql,(item['name'],item['rank'],item['country'],
                              item['state'],item['city'],item['undergraduate_num'],
                              item['postgraduate_num'],item['website']))    #执行上面sql语句
        '''
        cols=item.keys()
        values=[item[col] for col in cols]
        cols=['’%s‘' %key for key in cols]
        sql="INSERT INTO 'universities' ("+','.join(cols)+")"\
        "VALUES ("+','.join(['%s']*8)+ ")"
        self.cur.execute(sql,values)
        '''
        self.conn.commit()  #提交数据上去
        logger.info(self.cur._last_executed)
        logger.info('mysql: add %s to universities' % item['name'])
        return item

    def close_spier(self,spider):
        #当spider结束时，调用
        self.cur.close()
        self.conn.close()


