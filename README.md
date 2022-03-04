# Erocool Unofficial API
# Notice
This repository will not be updated.
The following has been moved to the following
<a href="https://github.com/dotinkasra/ErocoolAPI_nim">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=dotinkasra&repo=ErocoolAPI_nim" />
</a>
## How to use
・[日本語](https://github.com/Dotinkasra/ErocoolAPI/blob/main/README_ja.md)
### set
It takes the URL of the content as a parameter and sets it to the instance.

```python
from ErocoolAPI.api import ErocoolAPI

erocool = ErocoolAPI.set("https://ja.erocool.com/xxxxxxx/yyyyyy.html")
```

### info
Get the content information set in the instance using the set() method.

```python
erocool.info()
```

[Data](#Data) class will be returned.

| Option | Param | Type | Default | Description | 
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ✅ | display  | bool | False | Prints information about the content set in the instance.  |  

### download
Download the contents configured for the instance.  
By default, it will create a new directory with the title name of the content and download all the pages.  

```python
erocool.download()
```

The following is a list of options that can be given to this method.  
| Option | Param | Type | Default | Description | 
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ✅ | absolute_path  | str | None | Specify the destination of the content by absolute path.  |  
| ✅ | directory_name  | str | Title name of the content. | Rename the directory where the content will be saved.  | 
| ✅ | start | int | 1 |  Specify this option if you want to download from an arbitrary page. | 
| ✅ | end | int | Number of content pages. | The specified number of pages will be used as the last page. | 

### async_download
**<span style="color: red; ">Note: This is in the prototype stage.</span>**  

All arguments are the same as in the [download()](#download) method. Executes the download process asynchronously.

```python
erocool.async_download()
```

### search
Perform a search using keywords.  
This class is set up as a class method, so there is no need to create an instance when using it. 
However, some sites may not have it implemented, so please import the module for each site.

```python
from ErocoolAPI.api imoprt Erocool

keyword = ['JK', 'NTR']
Erocool.search(keyword)
```

The following is a list of options that can be given to this method.  
| Option | Param | Type | Default | Description | 
| ------------- | ------------- | ------------- | ------------- | ------------- | 
| ⬜️ | keyword  | str | None | Specify an array of keywords that are interesting to you.  | 
| ✅ | page  | int | 1 | If the search results span multiple pages, you can specify the page number you want to retrieve. |
| ✅ | ja_only | bool | True | Searches only for content in Japanese. | 
| ✅ | populer | bool | False | Search by popularity. By default, it is sorted by new arrivals. |

The return value is the [Result](#Result) class.

### ranking
Get the ranking of the content.  
This class is set up as a class method, so there is no need to create an instance when using it.  
However, some sites may not have it implemented, so please import the module for each site.

```python
from ErocoolAPI.api import Erocool

Erocool.ranking('daily')
```
You can select the period from the following  
 ```
 ['daily', 'weekly', 'monthly', 'history']
```

The return value is the [Result](#Result) class.

## Class

### Data
This is a dataclass that stores the results of parsing a content page.
| Property | Field | Type | Description | 
| ------------- | ------------- | ------------- | ------------- | 
| ✅ | ja_title | str | Japanese title. | 
| ✅ | en_title | str | English title.  |  
| ✅ | parodies | list[str] | Original content.  |  
| ✅ | tags | list[str] | Tags set for the manga.  |  
| ✅ | artists | list[str] | Author of the manga.  |  
| ✅ | groups | list[str] | Team name if written by a team of several people.  |  
| ✅ | lang | str | The language of manga.  |  
| ✅ | total_pages | int | Total number of manga pages  |  
| ✅ | upload_date | str | Submission date. Note: This is not necessarily the release date of the manga.  |  
| ✅ | thumbnail | str | URL of the manga thumbnail.  |  
| ✅ | url | str | The URL you set.  |  
### Result
This dataclass is for storing scraped data of search results using the search function of the site.

| Property　| Field | Type | Description | 
| ------------- | ------------- | ------------- | ------------- | 
| ✅ | pagination  | int | Number of pages of search results.  |
| ✅ | results  | list | Two-dimensional array. [{title,url},...]  |

## Commandline
You can use this API from the command line.
This requires that you have Python 3.9 or higher installed on your machine, with the modules described in the 'requirements.txt' section of this repository imported.
If you are using Venv, you can use it without any problem, but you need to activate it in a shell beforehand.

```bash
erocool 'https://ja.erocool.com/detail/xxxxxxx.html'
```

You can specify the page number to be saved, the path of the directory to be saved, and the directory name.

```bash
erocool 'https://ja.erocool.com/detail/xxxxxxx.html' -s 5 -e 10 -o ~/Downloads/Mangas -n 'xxxxx'
```

More information can be found with the -h option.


