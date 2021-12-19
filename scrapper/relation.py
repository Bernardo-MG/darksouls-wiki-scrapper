# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
import requests
from bs4 import BeautifulSoup
import logging

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class MerchantItemsRelScrapper(object):
    """
    Armor set relationships scrapper.
    """

    def __init__(self):
        super(MerchantItemsRelScrapper, self).__init__()
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


class MerchantItemsRelsScrapper(CsvScrapper):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self, root_url):
        super(MerchantItemsRelsScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Merchants',
                                                     'output/merchant_items.csv',
                                                     ['merchant', 'item'])
        self.inner_parser = ListScrapper(root_url, MerchantItemsRelScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
