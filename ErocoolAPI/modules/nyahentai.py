from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.schemas.result import Result

import urllib.parse 
import urllib.request
import re

class NyaHentai(Scraper):

    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __contents_page_analyze(self, url: str):
        self._data.url = url
        
        #タイトル取得
        self._data.ja_title = self.bs.select_one("#info > h1").text
        self._data.en_title = self.bs.select_one("#info > h2").text

        self._data.thumbnail = self.bs.select_one('#cover').find_all("img")[1].attrs['src']

        pagenation = self.bs.select_one("#info > div:nth-child(4)").text
        pagenation = str(pagenation).split()
        if pagenation is None:
            return 
        self._data.total_pages = int(pagenation[1])

        contents_id = re.findall(r'https://ja.nyahentai.(com|me)/g/(.*)/.*', url)[0]
        if contents_id is None:
            return

        src_list = []
        single_page_bs =  super()._Scraper__create_bs("https://ja.nyahentai.com/g/{contents_id}/list/1/#".format(contents_id = contents_id))
        gallery_url = single_page_bs.select_one("#image-container > a > img").attrs['src']
        base_gallery_url = re.findall(r'(https://.*/galleries/.*/).(\.png)',gallery_url)

        for i in range(pagenation):
            src = base_gallery_url[0][0] + str(i + 1) + base_gallery_url[0][1]
            src_list.append(src)
        
        self._data._image_list = src_list

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
