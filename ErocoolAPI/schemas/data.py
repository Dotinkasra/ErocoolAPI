import random
from dataclasses import dataclass
from dataclasses import field
@dataclass
class Data():
    _ja_title: str = str(random.randrange(10**6, 10**7))
    _en_title: str = ''
    _upload_date: str = ''
    _artists: list[str] = field(default_factory=list)
    _lang: str = ''
    _groups: list[str] = field(default_factory=list[str])
    _parodies: list[str] = field(default_factory=list[str])
    _tags: list[str] = field(default_factory=list[str])
    _total_pages: int = 0
    _thumbnail: str = ''
    _url: str = ''
    _image_list: list[str] = field(default_factory=list[str])
    
    @property
    def ja_title(self) -> str:
        return self._ja_title

    @ja_title.setter
    def ja_title(self, value):
        if value == None or value == '':
            return
        self._ja_title = value

    @property
    def en_title(self) -> str:
        return self._en_title

    @en_title.setter
    def en_title(self, value):
        self._en_title = value

    @property
    def upload_date(self) -> str:
        return self._upload_date

    @upload_date.setter
    def upload_date(self, value):
        self._upload_date = value

    @property
    def artists(self) -> list[str]:
        return self._artists

    @artists.setter
    def artists(self, value):
        self._artists = value

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def groups(self) -> list[str]:
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value

    @property
    def parodies(self) -> list[str]:
        return self._parodies

    @parodies.setter
    def parodies(self, value):
        self._parodies = value

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value) -> int:
        if type(value) is not int:
            self._total_pages = int(value)
        self._total_pages = value
    
    @property
    def thumbnail(self) -> str:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url

    @property
    def image_list(self) -> list[str]:
        return self._image_list

    @image_list.setter
    def image_list(self, value):
        if value == None:
            self._image_list = []
        self._image_list = value
    