create table users( 
    user_id SERIAL PRIMARY KEY
    , username varchar (20) NOT NULL
    , PRIMARY KEY (user_id) NOT NULL
); 

create table memos( 
    memo_id int
    , user_id int
    , title varchar (30)
    , summary varchar (30)
    , content text
    , PRIMARY KEY (memo_id)
    , FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- users テーブルにデータを挿入
INSERT INTO users (user_id, username) VALUES
(1, 'alice'),
(2, 'bob'),
(3, 'charlie'),
(4, 'diana'),
(5, 'eve');

-- memos テーブルにデータを挿入
INSERT INTO memos (memo_id, user_id, title, summary, content) VALUES
(1, 1, '買い物リスト', '週末の買い物', '牛乳、卵、パン、野菜を買うこと。'),
(2, 2, '会議メモ', '月曜の打合せ', '次回の開発ミーティングは10時から会議室Bで。'),
(3, 3, '旅行計画', '夏休み旅行', '京都に2泊3日で行く予定。ホテルと新幹線を予約する。'),
(4, 2, '読書メモ', '技術書の要点', '「Clean Code」の第1章をまとめる。'),
(5, 3, 'アイデアノート', '新アプリの構想', 'シンプルなメモ共有アプリを作るアイデア。');
