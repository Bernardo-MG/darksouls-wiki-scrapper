# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class AmmunitionDescriptionScrapper(CsvScrapper):
    """
    Ammunition list scrapper.
    """

    def __init__(self):
        super(AmmunitionDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Ammunition', 'output/ammunition.csv', ['name', 'description'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', DescriptionScrapper(), lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        return dom.select('td:nth-of-type(1) a:has(> img)')