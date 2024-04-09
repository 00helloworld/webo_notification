import sqlite3

db_name = 'data/database.db'
info_table = 'info_table'

def new_col(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN notify_flag TEXT;')

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    new_col(db_name, info_table)