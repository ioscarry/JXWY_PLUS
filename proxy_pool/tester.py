import aiohttp

from db import RedisClient

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100     # 设置批量测试的最大值

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self,proxy):   # 前面加async代表该方法是异步
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试',proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=5) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用',proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法',proxy)
            except (ClientError,ClientConnectorError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = aiohttp.asyncio.get_event_loop()
            # 批量测试
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy)for proxy in test_proxies]
                loop.run_until_complete(aiohttp.asyncio.wait(tasks))  # 使用aiohttp分配任务,启动运行异步检测.
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e.args)