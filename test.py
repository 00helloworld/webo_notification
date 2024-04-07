from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 设置 Chrome 选项
chrome_options = Options()

# 启用无头模式
chrome_options.add_argument("--headless")

# 添加隐藏 WebDriver 的特征的选项
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("blink-settings=imagesEnabled=false")
chrome_options.page_load_strategy = 'eager'


def save_html(driver, name='tmp'):
    html_content = driver.page_source
    with open(f'dev/{name}.html', 'w') as f:
        f.write(html_content)

def test(url="https://m.weibo.cn/u/2707458563"):
    # 从微博m版获取信息

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)

    driver.get(url)
    div_display = driver.find_element(by=By.CLASS_NAME, value='ProfileHeader_tag_2Ku6K')
    save_html(driver, name='test')

    # 关闭 WebDriver
    driver.quit()


if __name__ == '__main__':
    test('https://weibo.com/n/%E4%BB%BF%E4%BD%9B%E6%9C%B1%E8%8E%89%E8%8E%89')