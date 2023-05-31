import pymysql

mysql = pymysql.connect(
    host='xxx',
    user='xxx',
    password='xxx',
    db='xxx'
)

# 获取游标
cursor = mysql.cursor()
print('连接数据库OK')


class MySql:

    @classmethod
    def insert(cls, src, name, author, price):
        sql = f'insert into xxx (src, name, author, price) values(%s,%s,%s,%s);'
        cursor.execute(sql, (src, name, author, price))

    @classmethod
    def update(cls, src, name, author, price):
        sql = f'update xxx name={name},author={author},price={price} where set src={src};'
        cursor.execute(sql)
        mysql.commit()

    @classmethod
    def select(cls, src):
        sql = f'select * from xxx where src=%s;'
        cursor.execute(sql, src)
        mysql.commit()

    @classmethod
    def close(cls):
        cursor.close()
        mysql.close()
        print('数据库断开连接OK')
