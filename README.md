本项目基于Django1.11.14等来开发一个电商平台，可实现注册、登录、浏览、购买、支付等全部常用功能。

重点内容有：
Redis实现购物车记录存储
Redis实现最近浏览记录存储
发送注册邮件以Celery异步操作实现
网站优化之首页动态页面静态化——以Celery异步操作实现
网站优化之首页缓存——Redis存储
分布式存储系统FastDFS存储网站商品图片——自定义存储器类
商品搜索框架haystack
订单并发库存问题之悲观锁与乐观锁
自定义管理器实现快速查询数据
采用Django内置的认证系统进行登录校验——自定义用户类、校验装饰器
session基于Redis存储
支付宝接口
详细代码说明
运行环境：
见requirements.txt

代码中未有的常见问题：
一个常见的问题: mySQL里有2000w数据，redis中只存20w的数据，如何保证redis中的数据都是热点数据：

相关知识点：

redis 内存数据集大小上升到一定大小的时候，就会施行数据淘汰策略。
redis常见的六种淘汰策略：
volatile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰；
volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰；
volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰；
allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰；
allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰；
no-enviction（驱逐）：禁止驱逐数据。
限制用户短时间内登录次数的问题：

"""用列表实现:列表中每个元素代表登陆时间,只要最后的第5次登陆时间和现在时间差不超过1小时就禁止登陆"""
"""
请用Redis和任意语言实现一段恶意登录保护的代码，限制1小时内每用户Id最多只能登录5次
"""
import redis
import sys
import time

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
try:
    id = sys.argv[1]
except:
    print('input argument error')
    sys.exit(0)
# 将每次登陆的时间存入redis的名为login_item列表中，判断列表元素个数是否已达到5并且和第一次登录时间比较是否在一个小时以内。
if r.llen('login_item') >= 5 and (time.time() - float(r.lindex('login_item', 4)) <= 3600):
    print('you are forbidden logining')
else:
    print('you are allowed to login')
    r.lpush('login_item', time.time())
    
效果见：www.dongpouu.com
