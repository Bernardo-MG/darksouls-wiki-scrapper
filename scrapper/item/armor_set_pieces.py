# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests
from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import NameListScrapper


class ArmorSetPieceScrapper(object):
    """
    Armor set relationships scrapper.
    """

    def __init__(self):
        super(ArmorSetPieceScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Set
        set_name = dom.select('h1#firstHeading')[0].get_text()

        # Pieces
        pieces_list = dom.select('h2:has(span[id="set_pieces" i]) + ul a')
        pieces = list(map(lambda item: item['title'], pieces_list))

        data = []
        for piece in pieces:
            data.append({'armor': piece, 'set':set_name})

        return data


class ArmorSetPiecesScrapper(CsvScrapper):
    """
    Armor set relationships scrapper.
    """

    def __init__(self, root_url):
        super(ArmorSetPiecesScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)',
                                                     'output/armors_armor_sets.csv',
                                                     ['armor', 'set'])
        self.inner_parser = ListScrapper(root_url, ArmorSetPieceScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('div[title="Sets"] li a')