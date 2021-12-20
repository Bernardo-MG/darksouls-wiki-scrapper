# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class ArmorDescriptionScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ArmorDescriptionScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)', 'output/armors.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('table:not(:nth-of-type(1)) li a')