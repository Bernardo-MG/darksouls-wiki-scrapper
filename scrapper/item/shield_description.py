# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class ShieldDescriptionScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ShieldDescriptionScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shields.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')
