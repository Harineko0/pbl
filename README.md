# PBL 12班
[Gitのインストール方法(Windows版)](https://prog-8.com/docs/nodejs-env-win)

## Git
```shell
# リポジトリをクローン
git clone https://github.com/Harineko0/pbl

# <ブランチ名> は英数字か-, #, _などの記号のみ. 例: feat/send-email
git checkout -b feat/<ブランチ名>

# エディアでプログラムを編集

git add <ファイルを追加した場合,追加したファイルのパス>
git commit -am "変更内容を書いたメッセージ"
git push origin HEAD

# https://github.com/Harineko0/pbl にアクセスして GitHub 上でプルリクエストを作成
# Teams で誰かにレビュー依頼
# その後マージ

git checkout main
git pull origin main
```

## GAS
[スプレッドシート](https://docs.google.com/spreadsheets/d/1bHkE8b99HBAuce6jFvFRrIt-VLQVDCPXQQ4M423PSqQ/edit?gid=0#gid=0)  
[Windows 11 に Node.js をインストールしよう](https://qiita.com/nayoshik/items/c0febffab4a4b0ffb3b9)

環境構築, gas ディレクトリに移動して, ↓のコマンドを実行
```shell
npm install -g pnpm
pnpm install
```

スプレッドシートに変更を反映するときは, GitHub にプッシュするか, ローカルで次のコマンドを実行する
```shell
npm install -g @google/clasp
clasp login
clasp clone <スクリプトID>
```

### スクリプトID
1. スプレッドシートを開く
2. 拡張機能 -> App Script
3. 左側の歯車アイコンをクリック
4. ページの中部に スクリプトID がある

## Python
