import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import os
import hashlib  # 用于生成唯一ID避免重复条目

# 确保输出目录存在（适配工作流部署路径）
os.makedirs('output', exist_ok=True)

url = 'https://www.smg.gov.mo/smg/zawarning/index.php'

try:
    # 添加超时设置，避免无限等待
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 触发HTTP错误（如404、500）
except requests.exceptions.RequestException as e:
    print(f"网络请求错误: {e}")
    exit(1)

soup = BeautifulSoup(response.content, 'html.parser')

fg = FeedGenerator()
fg.title('澳门气象局预警信息')
fg.link(href=url)
fg.description('澳门气象局最新预警信息自动生成的RSS Feed')
fg.language('zh')

warnings = soup.find_all('div', class_='warning_content')

if not warnings:
    print("未找到预警信息")
else:
    for warning in warnings:
        text = warning.get_text(strip=True)
        if text:
            # 用内容哈希生成唯一ID，避免重复条目
            item_id = hashlib.md5(text.encode()).hexdigest()
            
            item = fg.add_entry()
            item.id(item_id)  # 唯一标识，避免重复
            # 用预警内容前20字作为标题，更具辨识度
            item.title(f'澳门气象预警：{text[:20]}...')
            item.link(href=url)
            item.description(text)
            # 使用UTC时间作为发布时间
            item.pubDate(datetime.utcnow())

# 生成到output目录，适配工作流部署路径
fg.rss_file('output/rss.xml')
