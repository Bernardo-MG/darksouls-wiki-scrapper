# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests
from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import NameListScrapper


class ShieldTypePieceScrapper(object):
    """
    Shield type relationships scrapper.
    """

    def __init__(self):
        super(ShieldTypePieceScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Type
        shield_type = dom.select('div[data-source="weapon-type"] div')[0].get_text()

        return {'shield': name, 'type': shield_type}


class ShieldTypePiecesScrapper(CsvScrapper):
    """
    Shield type relationships scrapper.
    """

    def __init__(self):
        super(ShieldTypePiecesScrapper, self).__init__('https://darksouls.fandom.com/wiki/Shields',
                                                     'output/shields_shield_types.csv',
                                                     ['shield', 'type'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', ShieldTypePieceScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')