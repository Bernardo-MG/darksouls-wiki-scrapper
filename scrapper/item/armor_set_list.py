# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class ArmorSetListScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(ArmorSetListScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)', 'output/armor_sets.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('table:nth-of-type(1) li a')