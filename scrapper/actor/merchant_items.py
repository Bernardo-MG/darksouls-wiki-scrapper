# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

from scrapper.base import CsvScrapper, ListScrapper


class MerchantItemScrapper(object):
    """
    Armor set relationships scrapper.
    """

    def __init__(self):
        super(MerchantItemScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Merchant
        merchant = dom.select('h1#firstHeading')[0].get_text()

        # Items
        items_list = dom.select('h2:has(span[id="Wares"]) + div small a[title]')
        self.logger.info('Item list %s', items_list)
        items = list(map(lambda info: info['title'], items_list))

        data = []
        for item in items:
            data.append({'merchant': merchant, 'item': item})

        return data


class MerchantItemsScrapper(CsvScrapper):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self):
        super(MerchantItemsScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Merchants',
                                                     'output/merchant_items.csv',
                                                     ['merchant', 'item'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', MerchantItemScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
