from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.schemas.Result import Result

import urllib.parse 
import urllib.request
import re

class NyaHentai(Scraper):

    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __contents_page_analyze(self, url: str):
        self._data['url'] = url
        
        #タイトル取得
        ja_title = self.bs.select_one("#info > h1").text
        en_title = self.bs.select_one("#info > h2").text

        self._data['ja_title'] = ja_title
        self._data['en_title'] = en_title

        thumbnail = self.bs.select_one('#cover').find_all("img")[1].attrs['src']

        self._data['thumbnail'] = thumbnail

        pagenation = self.bs.select_one("#info > div:nth-child(4)").text
        pagenation = str(pagenation).split()
        if pagenation is None:
            return 
        pagenation = int(pagenation[1])
        self._data['total_pages'] = pagenation

        contents_id = re.findall(r'https://ja.nyahentai.com/g/(.*)/.*', url)[0]
        if contents_id is None:
            return

        """    
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
            
            if head == 'タグ':
                self._data[subtitle[head]] = [x.text for x in body]
            elif head == '投稿日':
                self._data[subtitle[head]] = body[0]
            else:
                self._data[subtitle[head]] = body[0].text
        """
        src_list = []
        single_page_bs =  super()._Scraper__create_bs("https://ja.nyahentai.com/g/{contents_id}/list/1/#".format(contents_id = contents_id))
        gallery_url = single_page_bs.select_one("#image-container > a > img").attrs['src']
        base_gallery_url = re.findall(r'(https://.*/galleries/.*/).(\.png)',gallery_url)

        for i in range(pagenation):
            src = base_gallery_url[0][0] + str(i + 1) + base_gallery_url[0][1]
            src_list.append(src)
        
        self._image_list = src_list

    def __remove_escape(self, args: list) -> list:
        return [arg for arg in args if arg != '\n']


    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        self.check_url(r'https://ja.nyahentai.*.com/.*', url)
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
