# アプリケーションの概要

__毎日いくつもアラームを手動でオンオフすることから解放されます__

# アプリケーションの機能一覧

* ユーザーに _起きる時刻_、_アラームを鳴らし始める時刻_、_アラームを何分ごとに鳴らすか_、_アラームを何分鳴らし続けるか_ を設定してもらい、それをCSVファイルに書き込みます
* 設定した通りにアラームが鳴ります

![Alt text](/alarmer/documents/sample.JPG)

* 2回目以降は、そのCSVファイルを読み込み、過去の設定を再利用できます

![Alt text](/alarmer/documents/sample2.JPG)

# アプリケーション内で使用している技術一覧
* 言語はPython（テストコードを書くため、Pytestを使用しました）
* ソース管理はGit（Push, Fetch, Mergeの機能は使いました）

# 実行方法
1. 以下のURLからダウンロードするか、alarmerフォルダーとmain.pyを実行するディレクトリへ置いてください。

<https://drive.google.com/drive/folders/1Heomd6RbmRLieubFTgB1dbPO-FMohCbc?usp=sharing>

2. 以下のコマンドでインストールしてください。

_$ pip install termcolor_

_$ pip install pygame_

3. 以下のコマンドで実行して下さい。

_$ python main.py_

# オプション

1. 保存先のCSVファイルを変更したい場合は、実行するディレクトリにsettings.pyを作成し、以下をコピー&ペーストしてください。

_CSV_FILE_NAME='ここにファイル名を入れる'_

2. アラーム音を変更したい場合は、実行するディレクトリにsettings.pyを作成し、以下をコピー&ペーストしてください。

_MUSIC_FILE_NAME='ここにファイル名を入れる'_ (※再生可能な音声ファイルは、OGGファイルや非圧縮形式のWAVファイル、mp3ファイル等です。)
