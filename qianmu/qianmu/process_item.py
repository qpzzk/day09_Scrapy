import sys
import json
import logging
import redis
from pipelines import MysqlPipeline

r=redis.Redis()
logging.basicConfig()
logger=logging.getLogger('pipelines')
logger.info('begin to process item...')

def get_item(spider):
    key='%s:items' % spider
    item=r.blpop(key)        #会堵塞直到有一个值添加进来
    print('2222----------',item)  #将数据提取出来
    if item:
        return json.loads(item[1])  #将redis中的数据转换成json

if __name__=='__main__':
    if len(sys.argv) <2:
        logger.info('need spider name')
    spider=sys.argv[1]  #sys.argv是用来接受参数
    print('1111---------',spider)  #spider是u2
    db=MysqlPipeline()
    db.open_spider(spider)
    item=get_item(spider)  #最开始将数据插进去
    while item:
        db.process_item(item,spider)
        item=get_item(spider) #将新的数据进入循环插进去
    db.close_spier(spider)



