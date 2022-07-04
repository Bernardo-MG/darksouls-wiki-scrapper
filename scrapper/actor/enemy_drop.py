# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup


class AsideDropScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(AsideDropScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        drops = dom.select('aside[role="region"] div[data-source="drops"] a')
        drops = list(filter(lambda item: not 'None' == item['title'], drops))

        return list(map(lambda location: {'actor': name, 'location': location['title']}, drops))


class EnemyDropScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self):
        super(EnemyDropScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Enemies', 'output/enemy_drop.csv',
                                               ['actor', 'location'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', AsideDropScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))