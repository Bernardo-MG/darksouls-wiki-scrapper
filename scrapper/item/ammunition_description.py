# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class AmmunitionDescriptionScrapper(CsvScrapper):
    """
    Ammunition list scrapper.
    """

    def __init__(self, root_url):
        super(AmmunitionDescriptionScrapper, self).__init__(root_url + '/wiki/Ammunition', 'output/ammunition.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('td:nth-of-type(1) a:has(> img)')