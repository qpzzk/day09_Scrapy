import faker

class RandomUserAgentMiddleware(object):

    def __init__(self,setttings):
        #用faker设置一个可变的user-agent
        self.faker=faker.Faker()

    #从setting里面拿出内容
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_request(self,request,spider):
        request.headers['User-Agent']='%s' %self.faker.user_agent()+'zzk'*10