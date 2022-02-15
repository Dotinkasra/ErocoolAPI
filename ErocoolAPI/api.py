from ErocoolAPI.modules.erocool import Erocool
from ErocoolAPI.modules.caffe import Caffe
from ErocoolAPI.modules.nyahentai import NyaHentai
from ErocoolAPI.modules.ehentai import Ehentai
from ErocoolAPI.modules.dougle import Dougle
from ErocoolAPI.modules.scraper import Scraper
from ErocoolAPI.exceptions.exceptions import UnsupportedURLError

import re

class ErocoolAPI:

    @classmethod
    def set(self, url: str) -> Scraper:
        site = self.get_site(self, url)
        instance: Scraper = eval(site)()
        instance.set(url)
        return instance

    def get_site(self, url: str) -> str:
        support_sites = {
            'Erocool' : r'https://ja\.erocool.*\.com/.*',
            'Caffe' : r'https://eromanga.cafe\.com/.*',
            'NyaHentai' : r'https://ja.nyahentai.*.(com|me)/.*',
            'Ehentai' : r'https://e-hentai\.org.*',
            'Dougle' : r'https://dougle\.one/.*'
        }
        try:
            for site in support_sites:
                #対応サイトのURLと一致した場合
                if re.match(support_sites[site], url):
                    #適切なAPIのインスタンスを動的に返却する
                    return site
            #どのサイトにも一致しなかった場合は、自作例外を発生
            raise UnsupportedURLError("非対応サイト")
        except Exception as e:
            print(e)
    
