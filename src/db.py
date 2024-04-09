import sqlite3

def read_latest_info(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            username TEXT,
            followers TEXT,
            fans TEXT,
            signature TEXT,
            display_cnt TEXT,
            posts_cnt TEXT,
            create_date TEXT,
            create_time TEXT,
            error_flag TEXT,
            latest_flag TEXT,
            notify_flag TEXT,
            update_time TEXT
        )
    ''')

    cursor.execute(f"SELECT * FROM {table_name} WHERE latest_flag='YES'")
    latest_row = cursor.fetchone()
    if latest_row: 
        latest_data = {
            "username": latest_row[0],
            "followers": latest_row[1],
            "fans": latest_row[2],
            "signature": latest_row[3],
            "display_cnt": latest_row[4],
            "posts_cnt": latest_row[5],
            "create_date": latest_row[6],
            "create_time": latest_row[7],
            "error_flag": latest_row[8],
            "latest_flag": latest_row[9],
            "notify_flag": latest_row[10],
            "update_time": latest_row[11]
        }
    else:
        latest_data = {
            "username": 'no latest',
            "followers": 'no latest',
            "fans": 'no latest',
            "signature": 'no latest',
            "display_cnt": 'no latest',
            "posts_cnt": 'no latest',
            "create_date": 'no latest',
            "create_time": 'no latest',
            "error_flag": 'no latest',
            "latest_flag": 'no latest',
            "notify_flag": 'no latest',
            "update_time": 'no latest',
        }

    cursor.close()
    conn.close()

    return latest_data


def write_info(db_name, table_name, data):
    # data = {xx: xx}
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO {table_name} 
                   (username, followers, fans, signature, display_cnt, posts_cnt, create_date, create_time, error_flag, latest_flag, notify_flag, update_time) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                   , (data['username'], data['followers'], data['fans'], data['signature'], data['display_cnt'], data['posts_cnt'], 
                      data['create_date'], data['create_time'], data['error_flag'], data['latest_flag'], data['notify_flag'], data['update_time']))
    
    conn.commit()
    cursor.close()
    conn.close()


def update_info(db_name, table_name, data):
    # 记录更新时间和

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"UPDATE {table_name} SET latest_flag='NO', update_time=? WHERE latest_flag='YES'", (data['update_time'],))
    conn.commit()
    cursor.close()
    conn.close()
