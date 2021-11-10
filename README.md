# Erocool Unofficial API

## How to use
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

The values that can be obtained are as follows
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

The return value is a dict.  
These values can also be obtained on their own through properties.

### download
Download the contents configured for the instance.  
By default, it will create a new directory with the title name of the content and download all the pages.  

```python
erocool.download()
```

The following is a list of options that can be given to this method.  
| Param | Description | Default | 
| ------------- | ------------- | ------------- |
| absolute_path  | Specify the destination of the content by absolute path.  | None | 
| directory_name  | Rename the directory where the content will be saved.  | Title name of the content. |
| start | Specify this option if you want to download from an arbitrary page. | 1 |
| end | The specified number of pages will be used as the last page. | Number of content pages. |

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
| Param | Description | Default | 
| ------------- | ------------- | ------------- |
| keyword  | Specify an array of keywords that are interesting to you.  | - | 
| page  | If the search results span multiple pages, you can specify the page number you want to retrieve.  | 1 |
| ja_only | Searches only for content in Japanese. | True |
| populer | Search by popularity. By default, it is sorted by new arrivals. | False |

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
### Result
| Var | Type | Description | 
| ------------- | ------------- | ------------- | 
| pagination  | int | Number of pages of search results.  |
| results  | list | Two-dimensional array. [{title,url},...]  |

