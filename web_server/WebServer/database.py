import pymysql


def create_db(db_name='onlinelearning',
              host='127.0.0.1',
              account='root',
              port=3306,
              pd='123456',
              code='utf8'):
    conn = pymysql.connect(host=host, user=account, password=pd, charset=code, port=port)
    cursor = conn.cursor()

    cursor.execute('show databases;')
    data_tup = cursor.fetchall()
    if db_name.lower() in str(data_tup):
        print(f'data base {db_name} existed')
    else:
        cursor.execute(f'CREATE DATABASE {db_name} character set utf8;')


if __name__ == '__main__':
    create_db()
