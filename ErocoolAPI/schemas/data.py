import random
from dataclasses import dataclass
from dataclasses import field
@dataclass
class Data():
    _ja_title: str = str(random.randrange(10**6, 10**7))
    _en_title: str = field(default_factory=str)
    _upload_date: str = field(default_factory=str)
    _artists: list[str] = field(default_factory=list[str])
    _lang: str = field(default_factory=str)
    _groups: list[str] = field(default_factory=list[str])
    _parodies: list[str] = field(default_factory=list[str])
    _tags: list[str] = field(default_factory=list[str])
    _total_pages: int = field(default_factory=int)
    _thumbnail: str = field(default_factory=str)
    _url: str = field(default_factory=str)
    _image_list: list[str] = field(default_factory=list[str])
    
    @property
    def ja_title(self) -> str:
        return self._ja_title

    @ja_title.setter
    def ja_title(self, value: str):
        if value == None or value == '':
            return
        self._ja_title = value

    @property
    def en_title(self) -> str:
        return self._en_title

    @en_title.setter
    def en_title(self, value: str):
        self._en_title = value

    @property
    def upload_date(self) -> str:
        return self._upload_date

    @upload_date.setter
    def upload_date(self, value: str):
        self._upload_date = value

    @property
    def artists(self) -> list[str]:
        return self._artists

    @artists.setter
    def artists(self, value: list[str]):
        self._artists = value

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str):
        self._lang = value

    @property
    def groups(self) -> list[str]:
        return self._groups

    @groups.setter
    def groups(self, value: list[str]):
        self._groups = value

    @property
    def parodies(self) -> list[str]:
        return self._parodies

    @parodies.setter
    def parodies(self, value: list[str]):
        self._parodies = value

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, value: list[str]):
        self._tags = value

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value: int):
        if type(value) is not int:
            self._total_pages = int(value)
        self._total_pages = value
    
    @property
    def thumbnail(self) -> str:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value: str):
        self._thumbnail = value
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, url: str):
        self._url = url

    @property
    def image_list(self) -> list[str]:
        return self._image_list

    @image_list.setter
    def image_list(self, value: list[str]):
        if value == None:
            self._image_list = []
        self._image_list = value
    