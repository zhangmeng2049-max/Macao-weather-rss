import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

url = 'https://www.smg.gov.mo/smg/zawarning/index.php'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

fg = FeedGenerator()
fg.title('澳门气象局预警信息')
fg.link(href=url)
fg.description('自动生成的 RSS Feed')
fg.language('zh')

warnings = soup.find_all('div', class_='warning_content')

for idx, warning in enumerate(warnings):
    text = warning.get_text(strip=True)
    if text:
        item = fg.add_entry()
        item.title(f'预警 {idx + 1}')
        item.link(href=url)
        item.description(text)
        item.pubDate(datetime.utcnow())

fg.rss_file('rss.xml')
