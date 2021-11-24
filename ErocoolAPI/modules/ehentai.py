from pydantic import parse
from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.schemas.result import Result

import urllib.parse 
import urllib.request
import re

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
        if div_thumbnail_url is None or len(div_thumbnail_url) == 0:
            self._data.thumbnail = ''
        self._data.thumbnail = div_thumbnail_url[0]

        #作品の情報が記載されているtableから各種情報を抽出
        info_table = self.bs.select_one('#gdd > table')
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

        #画像ページを取得する
        image_page_div = self.bs.find_all('div', attrs={'class': 'gdtm'})
        for page in image_page_div:
            link = page.find_all('a')
            if link is None or len(link) ==0:
                continue
            single_page_bs = super()._Scraper__create_bs(link[0].attrs['href'])
            self._data._image_list.append(single_page_bs.select_one('#img').attrs['src'])
            del single_page_bs
        

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
