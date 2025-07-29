DROP DATABASE chatapp;
DROP USER 'nope_admin';

-- ユーザーとデータベースの作成
CREATE USER 'nope_admin'@'localhost' IDENTIFIED BY 'nope_admin';
CREATE DATABASE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'nope_admin'@'localhost';
FLUSH PRIVILEGES;

-- データベース選択
USE chatapp;

-- users テーブル
CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- rooms テーブル（DATETIMEに修正）
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_available BOOLEAN NOT NULL DEFAULT 0
);

-- user_rooms テーブル（スペルミス修正済）
CREATE TABLE user_rooms (
    uid VARCHAR(255) NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    PRIMARY KEY (uid, room_id)
);

-- messages テーブル（room → rooms修正済）
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(255) NOT NULL,
    room_id INT NOT NULL,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- 初期データ挿入
INSERT INTO users(uid, name, email, password)
VALUES (
    '970af84c-dd40-47ff-af23-282b72b7cca8',
    'テスト',
    'test@gmail.com',
    '37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578'
);

