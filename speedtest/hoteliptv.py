# -*- coding: utf-8 -*-
import sys
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 目标页面 URL
url = 'http://tonkiang.us/hoteliptv.php'

# 从命令行参数中获取搜索关键字
if len(sys.argv) < 2:
    print("Usage: python test.py <search_keyword>")
    sys.exit(1)

keyword = sys.argv[1]

# 构造 POST 请求参数
payload = {'search': keyword}

# 配置重试策略
retry_strategy = Retry(
    total=5,  # 总共重试次数
    status_forcelist=[500, 502, 503, 504],  # 针对这些状态码进行重试
    allowed_methods=["POST"],  # 针对 POST 请求进行重试
    backoff_factor=1  # 重试等待时间，1秒、2秒、4秒、8秒、16秒
)

# 配置 HTTPAdapter
adapter = HTTPAdapter(max_retries=retry_strategy)

# 创建会话
session = requests.Session()
session.mount("http://", adapter)

try:
    # 发送 POST 请求，设置超时时间为30秒
    response = session.post(url, data=payload, timeout=30)
    response.raise_for_status()  # 如果响应码不是200, 会抛出HTTPError异常
    # 打印响应内容
    print(response.text)
except requests.exceptions.Timeout:
    print("请求超时，请稍后再试。")
except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
