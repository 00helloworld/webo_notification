from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from src.log_config import info_logger, error_logger
# info_logger.info('This is crawler.py')
from confs import url_id


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

# 创建 Chrome WebDriver
# 注意：需要提前下载对应版本的 ChromeDriver，并指定其路径


def save_html(driver, name='tmp'):
    html_content = driver.page_source
    with open(f'dev/{name}.html', 'w') as f:
        f.write(html_content)


def get_info_m(url=f"https://m.weibo.cn/u/{url_id}"):
    # 从微博m版获取信息
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    driver.get(url)
    # time.sleep(10)
    save_html(driver, name='get_info_m')

    div_name = driver.find_element(by=By.CLASS_NAME, value='mod-fil-name')
    username = div_name.text
    weibo_web = f'https://weibo.com/n/{username}'
    div_fans = driver.find_element(by=By.CLASS_NAME, value="mod-fil-fans")
    followers = div_fans.find_element(by=By.XPATH, value="./div[@class='txt-shadow'][1]/span").text
    fans = div_fans.find_element(by=By.XPATH, value="./div[@class='txt-shadow'][2]/span").text
    p_signature = driver.find_element(by=By.CLASS_NAME, value="mod-fil-desc")
    signature = p_signature.text

    # 关闭 WebDriver
    driver.quit()

    return weibo_web, username, followers, fans, signature


def get_info_w(weibo_web):
    # 从微博web版获取信息

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(30)
    driver.get(weibo_web)
    # time.sleep(10)
    
    try:
        # 等待'全部微博（'出现
        element = WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.wbpro-screen-v2.woo-box-flex.woo-box-alignCenter.woo-box-justifyBetween'), '全部微博（')
        )
        info_logger.debug("等待'全部微博（'出现 Succeed")
    except:
        info_logger.debug("等待'全部微博（'出现 Fail")
        pass
    save_html(driver, name='get_info_w')
    div_display = driver.find_element(by=By.CLASS_NAME, value='ProfileHeader_tag_2Ku6K')
    display_cnt = div_display.text
    div_posts_cnt = driver.find_element(by=By.CSS_SELECTOR, value='div.wbpro-screen-v2.woo-box-flex.woo-box-alignCenter.woo-box-justifyBetween')
    posts_cnt = div_posts_cnt.text
    # 关闭 WebDriver
    driver.quit()

    return display_cnt, posts_cnt



if __name__ == '__main__':

    weibo_web, username, followers, fans, signature = get_info_m()
    display_cnt, posts_cnt = get_info_w(weibo_web)

    print(username, followers, fans, signature, display_cnt, posts_cnt)



