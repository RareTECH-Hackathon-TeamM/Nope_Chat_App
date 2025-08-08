from flask import abort
from flask_login import UserMixin
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()


class User(UserMixin):
    def __init__(self, uid, name, email, password):
        self.uid = str(uid)
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return self.uid

    @classmethod
    def create(cls, uid, name, email, password):
        conn = db_pool.get_conn()
        try:
            # コネクションからカーソル取得
            with conn.cursor() as cur:
                # SQLを実行し、データベースにユーザ情報を書き込む
                sql = "INSERT INTO users (uid, name, email, password) VALUES(%s, %s, %s, %s);"
                cur.execute(sql, (uid, name, email, password,))
                # DBに保存する
                conn.commit()
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_by_id(cls, uid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE uid=%s;"
                cur.execute(sql, (str(uid),))
                row = cur.fetchone()
                if row:
                    return cls(
                            row['uid'],
                            row['name'],
                            row['email'],
                            row['password']
                            )
                else:
                    return None
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_username(cls, name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE name=%s;"
                cur.execute(sql, (name,))
                row = cur.fetchone()
                if row:
                    return cls(
                            row['uid'],
                            row['name'],
                            row['email'],
                            row['password']
                            )
                else:
                    return None
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)


class Room:
    pass


class Message:

    @classmethod
    def last_sender(cls, name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # 今いてるルームの最後のメッセージの送信者を取得
                sql = ""
                cur.execute(sql, (name,))
                user = cur.fetchone()
                return user
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)
