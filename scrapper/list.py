# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from scrapper.base import BaseListScrapper

"""
Listing scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class EnemyScrapper(BaseListScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root):
        super(EnemyScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Enemies', 'output/enemies.csv', ['name'])

    def extract_list_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Thread:' in item['title'], result)

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        return {'name': name}
