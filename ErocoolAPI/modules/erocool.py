from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.schemas.result import Result

import urllib.parse 
import urllib.request
import re
#SSLエラー回避

class Erocool(Scraper):

    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __search_result_analyze(self, bs) -> Result:
        book_list = bs.select_one('#list > div.list-wrapper')
        pagination = bs.select_one('#list > ul:nth-child(2) > li:nth-child(5) > a')

        if pagination == None:
            pagination = 0
        else:
            pagination = int(pagination.attrs['data-ci-pagination-page'])

        results = []

        for data in book_list.find_all('a'):
            book = {}
            book['title'] = data.find_all('h3')[0].attrs['title']
            book['url'] = 'https://ja.erocool.com{}'.format(data.attrs['href'])
            results.append(book)

        return Result(pagination, results)

    def __contents_page_analyze(self, url: str):
        self._data.url = url
        
        #タイトル取得
        self._data.ja_title = self.bs.select_one("#comicdetail > h1").text
        self._data.en_title = self.bs.select_one("#comicdetail > h2").text

        thumbnail = self.bs.find_all("img", {'class': 'ld_thumbnail'})
        thumbnail = thumbnail[0].attrs['src']

        self._data.thumbnail = thumbnail

        ld_boxs_div = self.bs.select_one("div.listdetail_box.ldb2 > div.ld_boxs").contents
        ld_boxs_list = self.__remove_escape(ld_boxs_div)
        
        subtitle = {
            '原作' : 'parodies',
            'タグ' : 'tags',
            '作家' : 'artists',
            'サークル' : 'groups',
            '言語' : 'lang',
            '投稿日' : 'upload_date'
            }
            
        for div in ld_boxs_list:
            head = div.find_all('div', {'class': 'ld_head'})[0].contents[0]
            body = self.__remove_escape(div.find_all('div', {'class': 'ld_body'})[0].contents)
            if head not in subtitle:
                continue
            
            if head == '原作':
                self._data.parodies = body[0].text

            elif head == 'タグ':
                self._data.tags = [x.text for x in body]

            elif head == '作家':
                self._data.artists = [x.text for x in body]

            elif head == 'サークル':
                self._data.groups = [x.text for x in body]

            elif head == '言語':
                self._data.lang = body[0].text

            elif head == '投稿日':
                self._data.upload_date = body[0]

        src_list = []
        for item in self.bs.select_one("#comicdetail > div:nth-child(6)").find_all('img'):
            if not item.has_attr('data-src'):
                continue
            src_list.append(item.attrs['data-src'])
        
        self._data.total_pages = len(src_list)
        self._data.image_list = src_list

    def __remove_escape(self, args: list) -> list:
        return [arg for arg in args if arg != '\n']


    @classmethod
    def search(cls, keyword: list[str], page: int = 1, ja_only: bool = True, populer: bool = False):
        """Perform a keyword search.

        Args:
            keyword (list[str]): Keywords. If there are more than one, pass them as a list.
            page (int, optional): Specify which pages to display from multiple search results. Defaults to 1.
            ja_only (bool, optional): Searches only for content in Japanese. Defaults to True.
            populer (bool, optional): Search by popularity; if False, search by new. Defaults to False.

        Returns:
            Class: Class containing the search results. The properties to be retained are pagination and results. 
        """
        base_url = 'https://ja.erocool.com/search/q_{search_word}/page/{page}'
        ja_only_param = '%20japanese'
        populer_param = '/popular'
        
        #配列内のキーワードをパースして結合する。
        search_word = list(map(urllib.parse.quote, keyword))
        search_word = '%20'.join(search_word)

        #日本語のみを検索する場合
        if ja_only:
            search_word += ja_only_param

        #人気順で検索する場合
        if populer:
            search_word += populer_param

        url = base_url.format(search_word = search_word, page = str(page))

        bs = super()._Scraper__create_bs(cls, url)
        if bs == None:
            return 

        return cls.__search_result_analyze(cls, bs)

    @classmethod
    def ranking(cls, period: str = 'daily'):
        """Get the ranking. *Japanese only.

        Args:
            period (str, optional): Specify the period. The available options are ['daily', 'weekly', 'monthly', 'history']. Defaults to 'daily'.

        Returns:
            Class: Class containing the search results. The properties to be retained are pagination and results.
        """
        args = ['daily', 'weekly', 'monthly', 'history']
        if period not in args:
            period = 'daily'

        urls = {
            'daily' : 'https://ja.erocool.com/rank/day',
            'weekly' : 'https://ja.erocool.com/rank/week',
            'monthly' : 'https://ja.erocool.com/rank/month',
            'history' : 'https://ja.erocool.com/rank/history'
        }

        bs = super()._Scraper__create_bs(cls, urls[period])
        if bs == None:
            return 
        
        return cls.__search_result_analyze(cls, bs)

    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        self.check_url(r'https://ja.erocool.*.com/.*', url)
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
