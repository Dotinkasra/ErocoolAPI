import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint
from scraper import Scraper
import re

class CaffeAPI(Scraper):
    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __contents_page_analyze(self, url: str):
        #self.bs = BeautifulSoup()

        self._data['url'] = url
        self._data['lang'] = '日本語'

        self.bs.select_one("div.kijibox").find_all("p")[5].find_all("a")[0].attrs['href']

        main_contents = self.bs.select_one("div.kijibox").find_all("p")
        description = main_contents[0].text.split('\n')
        subtitle = {
            '作品名' : 'ja_title',
            'サークル名': 'groups',
            '元ネタ': 'parodies',
            '発行日' : 'upload_date',
            '漫画の内容' : 'tags'
        }

        for info in description:
            line = re.split(':|：', info)
            if line[0] not in subtitle:
                continue

            if subtitle[line[0]] == 'tags':
                self._data[subtitle[line[0]]] = [tag for tag in line[1].split(',')]
            else:
                self._data[subtitle[line[0]]] = line[1]

        src_list = []
        for content in main_contents:
            for a_tag in content.find_all('a'):
                if a_tag == None or not a_tag.has_attr('href'):
                    continue
                if re.search('http.://.*/.*jpg|.*png', a_tag.attrs['href']):
                    src_list.append(a_tag.attrs['href'])

        self._data['thumbnail'] = src_list[0]
        self._data['total_pages'] = len(src_list)
        self._image_list = src_list
        

    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        self.check_url(r'https://eromangacafe.com/.*', url)
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
    