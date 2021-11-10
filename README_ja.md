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

返却されるのは、以下の値を格納した辞書です。
 - ja_title
 - en_title
 - parodies
 - tags
 - artists
 - groups
 - lang
 - total_pages
 - upload_date
 - thumbnail
 - url

これらの値はpropatyを通じて個別に取得できます。

### download
インスタンスに設定されたコンテンツをダウンロードします。 
デフォルトでは、カレントディレクトリにコンテンツのタイトル名のディレクトリが新規作成され、すべてのページをダウンロードします。

```python
erocool.download()
```

以下のパラメータを指定できます。
| パラメータ | 説明 | デフォルト | 
| ------------- | ------------- | ------------- |
| absolute_path  | 保存先を絶対パスで指定する。  | None | 
| directory_name  | 保存するディレクトリの名前を指定する。  | コンテンツのタイトル |
| start | 途中のページからダウンロードしたい場合に、ページの開始番号を指定する。 | 1 |
| end | 途中のページまでダウンロードしたい場合に、ページの終了番号を指定する。 | コンテンツの最後のページ |


### search
キーワードで検索を行います。
classmethodのためインスタンス化をしなくても使用可能です。サイト毎に実装されていない場合があるので、個別にモジュールをインポートしてください。

```python
from ErocoolAPI.api imoprt Erocool

keyword = ['JK', 'NTR']
Erocool.search(keyword)
```

以下のパラメータを指定できます。
| パラメータ | 説明 | デフォルト | 
| ------------- | ------------- | ------------- |
| keyword  | 検索したいキーワードを配列に格納して指定します。必須。  | - | 
| page  | 検索結果が複数のページ分になる場合、取得したいページ番号を指定できます。  | 1 |
| ja_only | 日本語限定で検索します。 | True |
| populer | 人気順で検索します。デフォルトでは新着順で検索しています。 | False |

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
### Result
| 変数名 | 型 | 説明 | 
| ------------- | ------------- | ------------- | 
| pagination  | int | 検索結果のページ数です。  |
| results  | list | 二次元配列。 [{title,url},...]  |



