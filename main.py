
import setproctitle
setproctitle.setproctitle('weibocrawler')
import logging
from src.crawler import *
from src.db import *
from src.utils import *
from src.push import *

error_log = 'log/error.log'
success_log = 'log/success.log'
db_name = 'data/database.db'
info_table = 'info_table'


# 配置正常日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 创建一个新的文件处理程序（handler）用于记录正常日志
normal_file_handler = logging.FileHandler(success_log)
normal_file_handler.setLevel(logging.INFO)  # 设置级别为 INFO
normal_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 创建一个新的文件处理程序（handler）用于记录错误日志
error_file_handler = logging.FileHandler(error_log)
error_file_handler.setLevel(logging.ERROR)  # 设置级别为 ERROR
error_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 获取默认的日志记录器并添加处理程序
logger = logging.getLogger()
logger.addHandler(normal_file_handler)
logger.addHandler(error_file_handler)


def run():
    logger.info('run.py start')
    latest_data = read_latest_info(db_name, info_table)
    new_data = {}
    message = ''
    date_time, date, time = get_formatted_time()

    try:
        weibo_web, username, followers, fans, signature = get_info_m()
        logger.info('get_info_m() success')
        display_cnt, posts_cnt = get_info_w(weibo_web)
        logger.info('get_info_w() success')


    except Exception as e:
        logging.error(f"An error occurred in crawler.py: {e}", exc_info=True)
        message = 'error'

        error_flag = 'YES'
        latest_flag = 'NO'
        new_data = {
            "username": 'error',
            "followers": 'error',
            "fans": 'error',
            "signature": 'error',
            "display_cnt": 'error',
            "posts_cnt": 'error',
            "create_date": date,
            "create_time": time,
            "error_flag": error_flag,
            "latest_flag": latest_flag,
            "update_time": date_time
        }
        write_info(db_name, info_table, new_data)

        return message

    if latest_data["username"] != username:
        message = message + ' ' + f'用户名: {latest_data["username"]}->{username}'
        pass
    if latest_data["followers"] != followers:
        message = message + ' ' + f'关注: {latest_data["followers"]}->{followers}'
        pass
    if latest_data["fans"] != fans:
        message = message + ' ' + f'粉丝: {latest_data["fans"]}->{fans}'
        pass
    if latest_data["display_cnt"] != display_cnt:
        message = message + ' ' + f'播放量: {latest_data["display_cnt"]}->{display_cnt}'
        pass
    if latest_data["signature"] != signature:
        message = message + ' ' + f'签名: {latest_data["signature"]}->{signature}'
        pass
    if latest_data["posts_cnt"] != posts_cnt:
        message = message + ' ' + f'微博数量: {latest_data["posts_cnt"]}->{posts_cnt}'
        pass

    error_flag = 'NO'
    latest_flag = 'YES'
    new_data = {
        "username": username,
        "followers": followers,
        "fans": fans,
        "signature": signature,
        "display_cnt": display_cnt,
        "posts_cnt": posts_cnt,
        "create_date": date,
        "create_time": time,
        "error_flag": error_flag,
        "latest_flag": latest_flag,
        "update_time": date_time
    }
    latest_data['update_time'] = date_time
    update_info(db_name, info_table, latest_data)
    write_info(db_name, info_table, new_data)

    if len(message) > 5:
        logger.info('New changes appear')
    logger.info('run.py success')

    return message
    

    

if __name__=='__main__':

    try:
        message = run()
    except Exception as e:
        logging.error(f"An error occurred in run.py: {e}", exc_info=True)
        message = 'error'

    if message != '':
        try:
            status = pushover(message)
            logger.info('Message sent')
        except Exception as e:
            logging.error(f"An error occurred in pushover: {e}", exc_info=True)