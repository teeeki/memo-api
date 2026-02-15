# WebAPI
一覧（2026/2/15時点）
<img width="1383" height="599" alt="image" src="https://github.com/user-attachments/assets/3506c3d9-7ef5-4d71-a0d8-be73d7b5b77f" />

# メモの作成API
リクエストで送られたデータをDBへ保存

# メモの取得API
DBに登録されたメモ一覧を取得
※ 個別取得は未作成

# ユーザ登録API
ユーザIDとパスワードをDBに保存。
ただしパスワードはハッシュ化して保存。

# ログインAPI
リクエストで送られたユーザIDとパスワードを検証。
パスワードはハッシュ化して突き合わせる。
認証が成功したらアクセストークンを発行して返す。

## 環境構築
- python仮想環境の作成と有効化（PowerShell）
```bash
python -m venv share-memo
./share-memo/Scripts/activate
``` 

※ 仮想環境有効化に失敗した場合、PowerShellの実行ポリシーを変更する必要がある  
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

## FastAPIのインストール
```bash
pip install fastapi uvicorn
```

## FastAPIの起動
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
uvicorn main:app --reload // これはうまくいかない
``` 
