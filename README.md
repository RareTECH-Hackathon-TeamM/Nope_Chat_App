<h1 align="center">Nope - ノウプ</h1>
<br>
<img width="5334" height="3000" alt="Mチーム-2-1" src="https://github.com/user-attachments/assets/2c0c0633-dd30-47bc-baf2-95f20be81913" />

## コンセプト

「知り合ったばかりの人とLINE交換するの嫌じゃない？」

## アプリ概要

我々Team Mは、 "繋がりすぎる時代" にちょっと距離感のあるチャットアプリを考えました。\
LINEに友達登録されている人でこれ誰だったっけ？っていう方はいませんか？\
何年も前にたまたま会ってその場のノリでLINE交換したけど、その後一切連絡取らずに疎遠になった人、連絡網がわりのグループライン、こんな人会ったことあるっけ？と顔を見ても名前を見てもピンとこない人など・・・\
直近で連絡を取り合う必要があるなど、友達未満、知り合いレベルの方との連絡を取るためのアプリです。\

## ユーザの課題

「普段使いのチャットアプリはまだ教えたくない」、「SNSは私生活が知られるから嫌だ」、でも直近で連絡を取り合う必要があるなど、友達未満、知り合いレベルの方との連絡を取るためのアプリです。

## 機能一覧

```mermaid
---
config:
  layout: elk
  theme: neo
  look: neo
---
flowchart LR
    A("start") --> B["ログイン画面"]
    B -- 未登録 --> B_1["新規登録画面"]
    B -- 登録済み --> C["ホーム画面(ルーム一覧)"]
    B_1 --> C
    C <--> D["チャットルーム画面"]
    C -- ログアウト --> END("end")
```


## 仕様技術

| Category | Technology |
|----------|------------|
| Frontend | HTML, CSS, JavaScript, Jinja2 3.1.2 |
| Backend | Python3.11.3, Flask 2.3.3 |
| Infrastructure | --- |
| Database | MySQL 8.0 |
| Monitoring | --- |
| Environment setup | Docker |
| CI/CD | --- |
| Design | Figma |
| etc. | GitHub, Notion, Mattermost, ovice, mermaid |

## ER図

```mermaid
---
config:
  theme: neo
  look: neo
  layout: dagre
---
erDiagram
	direction TB
	users {
		uid VARCHAR(36) PK ""  
		name VARCHAR(20)  ""  
		email VARCHAR(70)  ""  
		password VARCHAR(60)  ""  
	}
	rooms {
		id VARCHAR(10) PK ""  
		name VARCHAR(20)  ""  
		room_type ENUM  ""
		is_available BOOLEAN  
		create_at TIMESTAMP  ""  
		update_at TIMESTAMP  ""  
	}
	messages {
		id VARCHAR(21) PK ""  
		uid VARCHAR(36) FK ""  
		room_id VARCHAR(10) FK ""  
		message VARCHAR(100)  ""  
		create_at TIMESTAMP  ""  
		update_at TIMESTAMP  ""  
	}
	user_rooms {
		uid VARCHAR(36) PK,FK ""  
		room_id VARCHAR(10) PK,FK ""  
	}
	users||--o{messages:"  "
	rooms||--o{messages:"  "
	users||--o{user_rooms:"  "
	rooms||--o{user_rooms:"  "
```

## 今後の展望
