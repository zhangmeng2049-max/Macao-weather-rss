import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import os
import hashlib

# 创建输出目录
os.makedirs('output', exist_ok=True)

# 澳门气象局预警页面URL
url = 'https://www.smg.gov.mo/smg/zawarning/index.php'

try:
    # 网络请求设置超时
    response = requests.get(url, timeout=15)
    response.raise_for_status()  # 处理HTTP错误
except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
    exit(1)

# 解析页面内容
soup = BeautifulSoup(response.content, 'html.parser')

# 初始化RSS生成器
fg = FeedGenerator()
fg.title('澳门气象局实时预警信息')
fg.link(href=url)
fg.description('自动抓取澳门气象局官网预警信息并生成的RSS订阅源')
fg.language('zh-CN')
fg.pubDate(datetime.utcnow())

# 提取预警信息
warnings = soup.find_all('div', class_='warning_content')

if warnings:
    for warning in warnings:
        content = warning.get_text(strip=True)
        if content:
            # 生成唯一ID避免重复条目
            item_id = hashlib.md5(content.encode()).hexdigest()
            
            # 创建RSS条目
            entry = fg.add_entry()
            entry.id(item_id)
            entry.title(f"澳门天气预警: {content[:20]}...")
            entry.link(href=url)
            entry.description(content)
            entry.pubDate(datetime.utcnow())
else:
    # 没有预警时添加提示信息
    entry = fg.add_entry()
    entry.id(f"no-alert-{datetime.utcnow().timestamp()}")
    entry.title("当前无澳门天气预警信息")
    entry.link(href=url)
    entry.description("澳门气象局目前未发布任何天气预警信号")
    entry.pubDate(datetime.utcnow())

# 保存RSS文件到output目录
fg.rss_file('output/rss.xml', pretty=True)
print("RSS文件生成成功")
os.makedirs('output', exist_ok=True) 和 fg.rss_file('output/rss.xml') 生成文件到 output
    
