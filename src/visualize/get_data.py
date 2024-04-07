import sqlite3
import pandas as pd
import arrow 

def get_table():
    # 获取当前日期和前2天的日期
    end_date = arrow.utcnow().format('YYYYMMDD')
    start_date = arrow.utcnow().shift(days=-2).format('YYYYMMDD')

    conn = sqlite3.connect('data/database.db')

    query = f"""
        SELECT * 
        FROM info_table 
        WHERE create_date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY update_time DESC;
    """
    df = pd.read_sql(query, con=conn)

    return df


def get_log(log_type):
    if log_type == 'info':
        file_path = 'log/success.log'
    else:
        file_path = 'log/error.log'

    last_20_lines = []
    with open(file_path, 'r') as file:
        # 使用for循环遍历文件内容
        for line in file:
            # 如果最后20行还没满，就将新的行添加到列表中
            if len(last_20_lines) < 20:
                last_20_lines.append(line.strip())
            else:
                # 如果最后20行已满，就删除第一行，然后添加新的行
                last_20_lines.pop(0)
                last_20_lines.append(line.strip())

    return last_20_lines
