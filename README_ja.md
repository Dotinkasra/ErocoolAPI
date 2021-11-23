# Erocool Unofficial API

## 使い方
### set
インスタンスにコンテンツの情報を設定します。

```python
from ErocoolAPI.api import ErocoolAPI

erocool = ErocoolAPI.set("https://ja.erocool.com/xxxxxxx/yyyyyy.html")
```

### info
set()メソッドを用いて設定された情報を取得します。

```python
erocool.info()
```

[Data](#Data) クラスが返却されます。

| オプション | パラメータ | 型 | デフォルト | 説明 | 
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ✅ | display  | bool | False | Dataクラスにセットされたデータを標準出力します。 |  

### download
インスタンスに設定されたコンテンツをダウンロードします。 
デフォルトでは、カレントディレクトリにコンテンツのタイトル名のディレクトリが新規作成され、すべてのページをダウンロードします。

```python
erocool.download()
```

以下のパラメータを指定できます。
| オプション | パラメータ | 型 | デフォルト | 説明 | 
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ✅ | absolute_path  | str | None | 絶対パスを指定した場合、そのパスに保存する。  |  
| ✅ | directory_name  | str | コンテンツのタイトル | 保存するディレクトリの名前を指定する。  | 
| ✅ | start | int | 1 | ダウンロードを開始するページ番号を指定する。 | 
| ✅ | end | int | コンテンツの最後のページ | ダウンロードを終了するページ番号を指定する。 | 


### async_download
**<span style="color: red; ">注意: テスト段階の機能です。</span>**  

全ての引数は [download()](#download) 関数と同様です。

```python
erocool.async_download()
```

### search
キーワードで検索を行います。
classmethodのためインスタンス化をしなくても使用可能です。サイト毎に実装されていない場合があるので、個別にモジュールをインポートしてください。

```python
from ErocoolAPI.api imoprt Erocool

keyword = ['JK', 'NTR']
Erocool.search(keyword)
```

以下のパラメータを指定できます。
| オプション | パラメータ | 型 | デフォルト | 説明 | 
| ------------- | ------------- | ------------- | ------------- | ------------- | 
| ⬜️ | keyword  | str | empty | 検索したいキーワードを配列に格納して指定します。  | 
| ✅ | page  | int | 1 | 検索結果が複数ページに渡る場合、取得したいページ番号を指定できます。 |
| ✅ | ja_only | bool | True | 日本語限定で検索します。 | 
| ✅ | populer | bool | False | 人気順で検索します。デフォルトでは新着順で検索しています。 |

戻り値は　[Result](#Result)クラス　です.

### ranking
ランキングを取得します。
classmethodのためインスタンス化をしなくても使用可能です。サイト毎に実装されていない場合があるので、個別にモジュールをインポートしてください。

```python
from ErocoolAPI.api import Erocool

Erocool.ranking('daily')
```

ランキングの期間は以下から選ぶことができます。
 ```
 ['daily', 'weekly', 'monthly', 'history']
```

戻り値は　[Result](#Result)クラス　です.

## クラス

### Data
漫画ページ解析情報格納用データクラス。

| プロパティ | フィールド | 型 | 説明 | 
| ------------- | ------------- | ------------- | ------------- | 
| ✅ | ja_title | str | 日本語のタイトル。 | 
| ✅ | en_title | str | 漫画の英題。  |  
| ✅ | parodies | list[str] | 漫画の元ネタ、原作。  |  
| ✅ | tags | list[str] | タグ（巨乳、NTR...等）。 |  
| ✅ | artists | list[str] | 作者一覧。  |  
| ✅ | groups | list[str] | サークル一覧。  |  
| ✅ | lang | str | 漫画の言語。  |  
| ✅ | total_pages | int | 漫画の総ページ数。  |  
| ✅ | upload_date | str | 投稿日。（※漫画の発売日であるとは限りません）  |  
| ✅ | thumbnail | str | サムネイルのURL。  |  
| ✅ | url | str | サイトのURL。  |  
### Result
検索結果解析情報格納用データクラス。

| プロパティ | フィールド | 型 | 説明 | 
| ------------- | ------------- | ------------- | ------------- | 
| ✅ | pagination  | int | 検索結果のページ数です。  |
| ✅ | results  | list | 二次元配列。 [{title,url},...]  |

## コマンドライン
コマンドラインからAPIを使用することができます。
実行する場合はPython 3.9以上がインストールされており、‘requirements.txt’に記述されたモジュールをインポートしておく必要があります。
Venvを使用している場合は、予めシェル上でアクティベートが必要です。

```bash
erocool 'https://ja.erocool.com/detail/xxxxxxx.html'
```

開始番号、終了番号、保存先、ディレクトリ名が指定できます。

```bash
erocool 'https://ja.erocool.com/detail/xxxxxxx.html' -s 5 -e 10 -o ~/Downloads/Mangas -n 'xxxxx'
```

オプションについての詳しい説明は -h オプションを参照してください。

