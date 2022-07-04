# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
import requests
from bs4 import BeautifulSoup

"""
Adjacent locations scrapper
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class AdjacentLocationScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(AdjacentLocationScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        locations = dom.select('h2:has(> span#Adjacent_locations) + ul a[title]')

        return list(map(lambda location: {'location': name, 'adjacent': location['title']}, locations))


class AdjacentLocationsScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self):
        super(AdjacentLocationsScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Locations', 'output/adjacent_locations.csv',
                                               ['location', 'adjacent'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', AdjacentLocationScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))

