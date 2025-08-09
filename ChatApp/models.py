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

    # ログイン時にDBに登録済みかの確認
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

    # 新規登録時にDBに登録済みかの確認
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

    # ログイン時、最終チャット日時が1か月以上経過していないかチェック
    # 経過しているユーザがいるときはroomを削除


class Room:
    @classmethod
    # HOME画面を開いたときフレンド名・最終メッセージ・最終メッセージの時間を取得
    def get_all_friends(cls, uid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                        SELECT
                            r.id AS room_id,
                            r.name AS room_name, -- DMではNULL
                            r.room_type, -- DMのみ
                            u.name AS friend_name,
                            m.message AS latest_message, -- 最新のメッセージ内容
                            m.created_at AS latest_time -- メッセージの時間
                        FROM
                            user_rooms ur_self
                        -- -----------------------------------
                        -- 自分が参加しているroom情報を結合
                        JOIN
                            rooms r ON ur_self.room_id = r.id
                        -- -----------------------------------
                        -- 同じroomにいる自分以外のユーザを取得
                        JOIN
                            user_rooms ur_friend ON ur_friend.room_id = r.id
                            AND ur_friend.uid != ur_self.uid
                        -- -----------------------------------
                        -- 相手ユーザのnameを取得
                        JOIN
                            users u ON u.uid = ur_friend.uid
                        -- -----------------------------------
                        -- 各ルームの最新メッセージの時間を取得
                        LEFT JOIN(
                            SELECT room_id, MAX(created_at) AS max_time
                        FROM messages
                        GROUP BY room_id
                        ) AS lm ON lm.room_id = r.id
                        -- -----------------------------------
                        -- 最新メッセージの時間に一致するmessageを1件だけ取得
                        LEFT JOIN
                            messages m ON m.room_id = r.id
                            AND m.created_at = lm.max_time
                        WHERE
                            ur_self.uid = %s
                        AND r.is_available = 1
                        AND r.room_type = 'dm'
                        -- -----------------------------------
                        -- 一番新しいメッセージのroomが上にくるように並べる
                        ORDER BY
                            lm.max_time DESC;
                    """
                cur.execute(sql, (uid,))
                rooms = cur.fetchall()
                return rooms
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_room(cls, friend_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    """
                cur.execute(sql, (friend_name,))
                rooms = cur.fetchall()
                return rooms
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # 友達追加を選択したときの招待側の処理
    @classmethod
    def add_room(cls, uid, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql_add_rooms = "INSERT INTO rooms (id) VALUES (%s);"
                sql_add_user_rooms = "INSERT INTO user_rooms (uid, room_id) VALUES (%s, %s);"
                cur.execute(sql_add_rooms, (room_id,))
                cur.execute(sql_add_user_rooms, (uid, room_id))
                # データベースに変更を反映（保存）する
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # user_roomsにレコードを追加する処理
    @classmethod
    def add_friend(cls, uid, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO user_rooms (uid, room_id) VALUES (%s, %s);"
                cur.execute(sql, (uid, room_id))
                # データベースに変更を反映(保存)する
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


class Message:
    def get_all_messages(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                        SELECT
                            u.name AS user_name,
                            m.message,
                            m.updated_at
                        FROM
                            messages AS m
                        -- -----------------------------------
                        -- user_nameを取得
                        JOIN
                            users u ON m.uid = u.uid
                        -- -----------------------------------
                        WHERE
                            m.room_id = %s
                        -- -----------------------------------
                        -- 一番新しいメッセージが下にくるように並べる
                        ORDER BY
                            m.updated_at;
                    """
                cur.execute(sql, (room_id,))
                rooms = cur.fetchall()
                return rooms
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # messagesにレコードを追加する処理
    @classmethod
    def add_message(cls, message_id, uid, room_id, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages (id, uid, room_id, message) VALUES (%s, %s, %s, %s);"
                cur.execute(sql, (message_id, uid, room_id, message))
                # データベースに変更を反映(保存)する
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def last_sender(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # 今いてるルームの最後のメッセージの送信者を取得
                sql = """
                    SELECT uid
                    FROM messages
                    WHERE room_id = %s
                    AND updated_at = (
                        SELECT MAX(updated_at)
                        FROM messages
                        WHERE room_id = %s
                        );
                    """
                cur.execute(sql, (room_id, room_id))
                user = cur.fetchone()
                return user
        except pymysql.Error as e:
            print(f'error: {e}')
            abort(500)
        finally:
            db_pool.release(conn)
