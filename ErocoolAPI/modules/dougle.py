from ErocoolAPI.modules.scraper import Scraper
import re

class Dougle(Scraper):
    def __init__(self, user_agent = None) -> None:
        super().__init__(user_agent)

    def __contents_page_analyze(self, url: str):
        #self.bs = BeautifulSoup()

        self._data.url = url
        self._data.lang = '日本語'
        self._data.ja_title = self.bs.find_all('h1', attrs={'class': 'single-post-title entry-title'})[0].text

        tag_area = self.bs.find_all('div', attrs={'class': 'tag_area'})
        if len(tag_area) == 2:
            [self._data.artists.append(x.text) for x in tag_area[0].find_all('div')]
            [self._data.tags.append(x.text) for x in tag_area[1].find_all('div')]

        for a in self.bs.find_all('div', attrs={'class': 'content'})[0].find_all('a'):
            if re.match(r'http.://.*/(.*jpg|.*png)', a.attrs['href']):
                self._data.image_list.append(a.attrs['href'])
            else:
                continue
        self._data.total_pages = len(self._data.image_list)
        self._data.thumbnail = self._data.image_list[0]

    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
    