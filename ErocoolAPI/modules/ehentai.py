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
        pass

    def __remove_escape(self, args: list) -> list:
        return [arg for arg in args if arg != '\n']


    def set(self, url: str):
        """Set the information of the comic to this instance.

        Args:
            url (str): URL of the manga page.
        """
        self.bs = super()._Scraper__create_bs(url)
        if self.bs == None:
            return None

        self.__contents_page_analyze(url)
