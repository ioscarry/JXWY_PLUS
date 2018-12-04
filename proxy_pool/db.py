MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import redis
from random import choice

# zset有序集合通过score值排序
# REDIS_KEY是有序集合的键名, 我们可通过它来获取代理存储所使用的有序集合.
class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,db=1):
        self.db = redis.StrictRedis(host=host,port=port,db=db,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        # 添加代理,设置默认分数
        if not self.db.zscore(REDIS_KEY,proxy):  # 如果该value没有score值
            return self.db.zadd(REDIS_KEY.score,proxy)

    def random(self):
        # 随机获取有效代理
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)  # 返回分数范围的经过排序的值
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100)    # 返回下标0-100的值, 降序排列(排名前100的随机代理)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self,proxy):
        # 代理值减一分, 分数小于最小值则代理删除
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,proxy,-1) # 通过zincrby方法增减score的值
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        # 判断代理是否存在于集合中
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def max(self,proxy):
        # 若代理有效,将代理设置为MAX_SCORE
        print('代理',proxy,'可用,设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        # 获取数量
        return self.db.zcard(REDIS_KEY)

    def all(self):
        # 获取全部代理
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

# if __name__ == '__main__':
#     rediss=RedisClient('127.0.0.1','6379')
    # print(rediss.add())