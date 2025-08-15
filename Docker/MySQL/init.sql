DROP DATABASE chatapp;
DROP USER 'nope_admin';


CREATE USER 'nope_admin' IDENTIFIED BY 'nope_admin';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'nope_admin';

-- データベース選択
USE chatapp;

-- users テーブル
CREATE TABLE users (
    -- --------------------------------------------
    -- uidをUUID4で生成36文字
    uid VARCHAR(36) NOT NULL PRIMARY KEY,
    -- --------------------------------------------
    -- 最大20文字
    name VARCHAR(20) UNIQUE NOT NULL,
    -- --------------------------------------------
    -- 最大70文字outlook(70), Gmail(40)etc...(概算)
    email VARCHAR(70) UNIQUE NOT NULL,
    -- --------------------------------------------
    -- バージョン4 + コスト3 + ソルト22 + ハッシュ31 = 計60文字
    password VARCHAR(60) NOT NULL
);

-- rooms テーブル
CREATE TABLE rooms (
    -- --------------------------------------------
    -- room_idをNanoIDで生成10文字
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    -- --------------------------------------------
    -- グループトーク用
    name VARCHAR(20) DEFAULT NULL,
    -- --------------------------------------------
    -- 次回versionでグループトーク追加の検討
    room_type ENUM('dm', 'group') NOT NULL DEFAULT 'dm',
    -- --------------------------------------------
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- ---------------------------------------------
    -- フレンド誤削除に復元可能にする
    -- 削除フラグ: アクティブか否か1=True, 0=False
    is_available BOOLEAN NOT NULL DEFAULT 1
);

-- user_rooms テーブル
CREATE TABLE user_rooms (
    -- --------------------------------------------
    uid VARCHAR(36) NOT NULL,
    -- --------------------------------------------
    room_id VARCHAR(10) NOT NULL,
    -- --------------------------------------------
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    PRIMARY KEY (uid, room_id)
);

-- messages テーブル
CREATE TABLE messages (
    -- --------------------------------------------
    -- idをNanoIDで生成21文字
    id VARCHAR(21) NOT NULL PRIMARY KEY,
    -- --------------------------------------------
    uid VARCHAR(36) NOT NULL,
    -- --------------------------------------------
    room_id VARCHAR(10) NOT NULL,
    -- --------------------------------------------
    -- 100文字制限(アプリの仕様)
    message VARCHAR(100) NOT NULL,
    -- --------------------------------------------
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- --------------------------------------------
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- 初期データ挿入
INSERT INTO users(uid, name, email, password)
VALUES
    ('970af84c-dd40-47ff-af23-282b72b7cca8',
    'テスト',
    'test@gmail.com',
    '$2b$12$.h0.pTvtyc.tPczzxa94..zYGqN1Q/ZsBrFZaKqdFFmVedgHF2VNm'),
    ('970af84c-dd40-47ff-af23-282b72b7cca9',
    'テスト2',
    'test2@gmail.com',
    '$2b$12$IrCRto1vY6RuJt16iqnUHeJkXShE3DmYchD36BzsbC8w88hgci7g6'),
    ('970af84c-dd40-47ff-af23-282b72b7ccaa',
     'テスト3',
     'test3@gmail.com',
     '$2b$12$nKU2sfW8jc2gRO2F9BJXku92x7IlNfG2RpLwM6q5qKjTY6V7j5bnW'),
    ('970af84c-dd40-47ff-af23-282b72b7ccab',
     'テスト4',
     'test4@gmail.com',
     '$2b$12$ZyM9aCeZgFllP5llwPCc9exgJ4U8hHvhmLRD5CIyM9YzK4/WgR35a');

INSERT INTO rooms(id, name, room_type) VALUES
  ('WMDEceZq8G', NULL, 'dm'),     -- id=1
  ('QyGGMfNp7s', NULL, 'dm');   -- id=2

-- ルーム1: テスト, テスト2
INSERT INTO user_rooms(uid, room_id) VALUES
  ('970af84c-dd40-47ff-af23-282b72b7cca8', 'WMDEceZq8G'),
  ('970af84c-dd40-47ff-af23-282b72b7cca9', 'WMDEceZq8G');

-- ルーム2: テスト3, テスト4
INSERT INTO user_rooms(uid, room_id) VALUES
  ('970af84c-dd40-47ff-af23-282b72b7ccaa', 'QyGGMfNp7s'),
  ('970af84c-dd40-47ff-af23-282b72b7ccab', 'QyGGMfNp7s');

-- ルーム1: テスト <-> テスト2
INSERT INTO messages(id, uid, room_id, message) VALUES
  ('ky3axowgi6QHAL6FZ33Y3', '970af84c-dd40-47ff-af23-282b72b7cca8', 'WMDEceZq8G', 'こんにちは、テスト2さん'),
  ('p00mHjG24JnwyEY1Rqw65', '970af84c-dd40-47ff-af23-282b72b7cca9', 'WMDEceZq8G', 'こんにちは、テストさん！元気ですか？'),
  ('ShaU31ygO0mU5kz5WrICZ', '970af84c-dd40-47ff-af23-282b72b7cca8', 'WMDEceZq8G', 'テスト2さん、元気です！テスト2さんは？'),
  ('gpPpD0arW2LNGihUX6uaA', '970af84c-dd40-47ff-af23-282b72b7cca9', 'WMDEceZq8G', '元気です！');

-- ルーム2: テスト3 <-> テスト4
INSERT INTO messages(id, uid, room_id, message) VALUES
  ('RTh2IWRaagysNBrNZL9QW', '970af84c-dd40-47ff-af23-282b72b7ccaa', 'QyGGMfNp7s', '今日の打ち合わせは何時ですか？'),
  ('Byla1mOoe70Lz-cMiwKn4', '970af84c-dd40-47ff-af23-282b72b7ccab', 'QyGGMfNp7s', '15時からでお願いします');

