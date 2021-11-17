from ErocoolAPI.modules.erocool import Erocool
from ErocoolAPI.modules.caffe import Caffe
from ErocoolAPI.modules.nyahentai import NyaHentai
from ErocoolAPI.exceptions.exceptions import UnsupportedURLError

import re

class ErocoolAPI:
    @classmethod
    def set(self, url: str):
        site = self.get_site(self, url)
        instance = eval(site)()
        instance.set(url)
        return instance

    def get_site(self, url: str):
        support_sites = {
            'Erocool' : r'https://ja\.erocool.*\.com/.*',
            'Caffe' : r'https://eromangacafe\.com/.*',
            'NyaHentai' : r'https://ja.nyahentai.*.com/.*'
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