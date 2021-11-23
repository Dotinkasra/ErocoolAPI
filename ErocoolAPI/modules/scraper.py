from ErocoolAPI.exceptions.exceptions import UnsupportedURLError
from ErocoolAPI.schemas.data import Data

import ssl
import os
import urllib.parse 
import urllib.request
import urllib.error
import re
import random
import asyncio
import tqdm
from pprint import pprint
from typing import Pattern
from bs4 import BeautifulSoup
from abc import abstractmethod
#import traceback
#import functools
#from abc import ABCMeta, abstractmethod, abstractclassmethod

class Scraper:
    ssl._create_default_https_context = ssl._create_unverified_context
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
    headers = {
            "User-Agent": user_agent,
    }

    def __init__(self, user_agent = None) -> None:
        if not user_agent == None:
            self.user_agent = user_agent

        self.headers = {
            "User-Agent": self.user_agent,
        }
        self._data = Data()
    
    # bsによってパースされたHTMLを返却するメソッド
    # 引数：URL（文字列）
    # 返り値:受け取ったURLを引数として与えたBeautifulSoupインスタンス
    def __create_bs(self, url: str) -> BeautifulSoup:
        try:
            request = urllib.request.Request(url = url, headers = self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8', 'ignore')
            soup = BeautifulSoup(html, "lxml")
        except Exception as e:
            print(e)
            print(url)
        else:
            return soup

    def __remove_escape(self, args: list) -> list:
        return [arg for arg in args if arg != '\n']

    def __downloader(self, download_url: str, dst_path: str):
        req = urllib.request.Request(url = download_url, headers = self.headers)
        data = urllib.request.urlopen(url = req, timeout = 4.0).read()
        with open(dst_path,mode="wb") as f:
            f.write(data)

    @abstractmethod
    def __contents_page_analyze(self, url: str) -> dict:
        """ページをスクレピングするメソッド。必ずself._dataとself._image_listを設定すること。

        Args:
            url (str): [サイトのURL]

        Returns:
            dict: ['ja_title', 'en_title', 'parodies', 'tags', 'artists', 'groups', 'lang', 'total_pages', 'upload_date', 'thumbnail', 'url']
        """
        pass
    
    def check_url(self, pattern: Pattern, url: str) -> bool:
        if re.match(pattern, url):
            return True
        else:
            raise UnsupportedURLError('対応していないURLです')

    def parse_title(self, title: str) -> str:
        return title.translate(str.maketrans({'/' : '', '　':'', ' ': ''}))
        #return title.replace('/', '')

    @abstractmethod
    def set(self, url: str):
       pass
    
    def info(self) -> Data:
        """Get the information of the manga set in this instance.

        Returns:
            dict[str]: Information about the manga.
        """
        return self._data

    def get_image_url(self, url: str) -> str:
        re.findall('http.://.*/(.*jpg|.*png)', url)[0]

    def download(self, absolute_path: str = None, directory_name: str = None, start: int = 1, end: int = None):
        """Download the manga set for this instance.

        Args:
            absolute_path (str, optional): Argument for specifying an absolute path. Defaults to None.
            directory_name (str, optional): This is an argument that specifies the name of the directory to save the comic. Defaults to None.
            start (int, optional): Start number of the page you want to download. Defaults to 1.
            end (int, optional): The last number of the page you want to download. Defaults to None. The default is to download to the end of the page.
        """
        if self.bs == None:
            return 

        dir_path = absolute_path
        dir_name = directory_name

        if dir_path == None:
            dir_path = './'

        if dir_name == None:
            dir_name = self._data.ja_title if not (self._data.ja_title == None or self._data.ja_title == '') else str(random.randrange(10**6, 10**7))

        dir_path = os.path.join(dir_path, dir_name)

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok = True)

        if end == None:
            end = self._data.total_pages
            
        # ページの画像表示divを取得
        #image_list = self.bs.select_one("#comicdetail > div:nth-child(6)").find_all('img')
        if len(self._data.image_list) == 0:
            return 

        # 画像の数だけループする
        for i, item in enumerate(self._data.image_list):
            #if not item.has_attr('data-src'):
            #    continue
            #src_link = item.attrs['data-src']
            # 保存用のファイル名を生成する
            file_name = "hcooldl_{:0>3}_".format(str(i + 1)) + self.get_image_url(item)
            
            if i + 1 < start:
                continue
            if i + 1 > end:
                break

            #dst_path = dir_path + '/' + file_name
            dst_path = os.path.join(dir_path, file_name)
            
            try:
                # ダウンロードを実行する
                self.__downloader(item, dst_path)
            except urllib.error.HTTPError as e:
                print(e)
            except Exception as e:
                print(e)

    def async_download(self, absolute_path: str = None, directory_name: str = None, start: int = 1, end: int = None):
        """Download the manga set for this instance.

        Args:
            absolute_path (str, optional): Argument for specifying an absolute path. Defaults to None.
            directory_name (str, optional): This is an argument that specifies the name of the directory to save the comic. Defaults to None.
            start (int, optional): Start number of the page you want to download. Defaults to 1.
            end (int, optional): The last number of the page you want to download. Defaults to None. The default is to download to the end of the page.
        """
        if self.bs == None:
            return 
        loop = asyncio.new_event_loop()

        dir_path = absolute_path
        dir_name = directory_name

        if dir_path == None or dir_path == '':
            dir_path = './'

        if dir_name == None or dir_name == '':
            dir_name = self._data.ja_title if not (self._data.ja_title == None or self._data.ja_title == '') else str(random.randrange(10**6, 10**7))

        self.dir_path = os.path.join(dir_path, dir_name)

        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path, exist_ok = True)

        if end == None:
            end = self._data.total_pages
            
        # ページの画像表示divを取得
        #image_list = self.bs.select_one("#comicdetail > div:nth-child(6)").find_all('img')
        if len(self._data.image_list) == 0:
            return 
        
        do_download_img = []

        # 画像の数だけループする
        for i, item in enumerate(self._data.image_list):
            #if not item.has_attr('data-src'):
            #    continue
            #src_link = item.attrs['data-src']

            if i + 1 < start:
                continue
            if i + 1 > end:
                break
            do_download_img.append(item)

            
        loop.run_until_complete(self.handler(loop, do_download_img))
        loop.close()


    async def handler(self, loop, image_list):
        async def exec(i):
            # 並列制限を2に設定
            async with asyncio.Semaphore(3):
                return await loop.run_in_executor(None, self.__async_downloader , i)
        tasks = [exec(i) for i in image_list]
        #return await asyncio.gather(*tasks)
        for t in tqdm.tqdm(asyncio.as_completed(tasks), desc="Downloading...", total=len(image_list)):
            await t

    def __async_downloader(self, download_url: str):
        file_name = "hcooldl_" + re.findall('http.://.*/(.*jpg|.*png)', download_url)[0]
        try:
            dst_path = os.path.join(self.dir_path, file_name)
            req = urllib.request.Request(url = download_url, headers = self.headers)
            data = urllib.request.urlopen(url = req, timeout = 4.0).read()
            with open(dst_path,mode="wb") as f:
                f.write(data)
        except Exception :
            return