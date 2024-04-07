import requests
from bs4 import BeautifulSoup


url = 'https://m.weibo.cn/u/2707458563'
re = requests.get(url)

print(re.status_code)

with open('dev/tmp.html', 'w') as f:
    f.write(re.text)

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(re.text, 'html.parser')
# 找到 class 名为 "mod-fil-name m-txt-cut" 的 <div>
div = soup.find('div', class_='mod-fil-name m-txt-cut')
# 从 <div> 中找到包含文本 "仿佛朱莉莉" 的 <span>
span = div.find('span', class_='txt-shadow')
print(span.text)