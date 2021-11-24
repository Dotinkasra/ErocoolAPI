from bs4 import BeautifulSoup
from pydantic import parse
from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.schemas.result import Result

import urllib.parse 
import urllib.request
import re
import asyncio

class Ehentai(Scraper):

    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __contents_page_analyze(self, url: str):
        self._data.url = url
        
        #タイトル取得
        self._data.ja_title = self.bs.select_one('#gn').text

        #サムネイルのURLを取得（HTMLでURL関数の中に書かれているので正規表現で抽出
        div_thumbnail_style = self.bs.select_one('#gd1 > div').attrs['style']
        div_thumbnail_url = re.findall(r'.*url\((https://.*)\)',  div_thumbnail_style)

        if self.is_vaild_as_list(div_thumbnail_url):
            self._data.thumbnail = div_thumbnail_url[0]
        else:
            self._data.thumbnail = ''

        #作品の情報が記載されているtableから各種情報を抽出
        self.__set_infomation(bs=self.bs)

        #全ページ実行する
        all_page = self.__get_all_gallery_page_url(bs=self.bs)
        if not self.is_vaild_as_list(all_page):
            return

        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(self.__get_viewer_link_loop_handler(loop, all_page))
        all_viewer_link = [link for row in result for link in row]

        loop.run_until_complete(self.__set_image_link_loop_handler(loop, all_viewer_link))
        loop.close()

    #BSオブジェクトを元にe-hentaiページから情報を抽出し、Dataクラスへセットする
    def __set_infomation(self, bs: BeautifulSoup):
        info_table = bs.select_one('#gdd > table')
        info_table_rows = info_table.find_all('tr')

        #テーブルの1行ずつループ
        if info_table_rows is not None and len(info_table_rows) > 0:

            for info_table_row in info_table_rows:
                info_table_data = info_table_row.find_all('td')

                if info_table_data is None or len(info_table_data) ==0:
                    continue

                if info_table_data[0].text == 'Posted:':
                    self._data.upload_date = info_table_data[1].text

                elif info_table_data[0].text == 'Language:':
                    self._data.lang = info_table_data[1].text

                elif info_table_data[0].text == 'Length:':
                    page_num = re.sub(r'\D', '', info_table_data[1].text)
                    self._data.total_pages = int(page_num)

    #ギャラリーページのページ数を取得し、URL一覧を返却する
    def __get_all_gallery_page_url(self, bs: BeautifulSoup) -> list[str]:
        page_url_links = []
        pagenation_table = bs.select_one('body > div:nth-child(9) > table')
        if self.is_vaild_as_list(pagenation_table):
            pagenation_table_row = pagenation_table.find_all('tr')[0]
            for page in pagenation_table_row:
                a = page.find_all('a')
                if not self.is_vaild_as_list(a):
                    continue
                page_url_links.append(a[0].attrs['href'])
        return list(set(page_url_links))

    #e-hentaiのギャラリーページから画像表示ページへのリンクを抽出する
    def __get_viewer_link(self, url: str) -> list[str]:
        link_list = []
        single_page_bs = super()._Scraper__create_bs(url)
        image_page_div = single_page_bs.find_all('div', attrs={'class': 'gdtm'})
        for page in image_page_div:
            link = page.find_all('a')
            if not self.is_vaild_as_list(link):
                continue
            if link[0].attrs['href']:
                link_list.append(link[0].attrs['href'])
        del single_page_bs
        return link_list

    #e-hentaiの画像表示ページから画像のリンクを抽出する
    def __set_image_link(self, url: str):
        single_page_bs = super()._Scraper__create_bs(url)
        link = single_page_bs.select_one('#img').attrs['src']
        if link:
            self._data._image_list.append(link)
        del single_page_bs

    async def __get_viewer_link_loop_handler(self, loop, target):
        async def exec(i):
            async with asyncio.Semaphore(3):
                return await loop.run_in_executor(None, self.__get_viewer_link , i)
        tasks = [exec(i) for i in target]
        return await asyncio.gather(*tasks)

    async def __set_image_link_loop_handler(self, loop, target):
        async def exec(i):
            async with asyncio.Semaphore(3):
                return await loop.run_in_executor(None, self.__set_image_link , i)
        tasks = [exec(i) for i in target]
        return await asyncio.gather(*tasks)

    def __remove_escape(self, args: list) -> list:
        return [arg for arg in args if arg != '\n']


    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        #self.check_url(r'https://ja.nyahentai.*.com/.*', url)
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
