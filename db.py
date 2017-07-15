
# db连接信息
HOST = 'localhost'
PORT = 6379

# 代理池大小
proxy_pool = 50

# 检测代理池的周期时间
times = 1200


# 基础设置
# 请求头信息
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

# 测试的url
test_url = 'http://www.nyist.net/'



# 代理池的容量控制开关
PROXY_VOLUME_CONTROL = True

# 代理池中可用ip检测开关
PROXY_AVAILABLE_CONTROL = True
