# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class PyromancyDescriptionScrapper(CsvScrapper):
    """
    Pyromancy list scrapper.
    """

    def __init__(self):
        super(PyromancyDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Pyromancy_(Dark_Souls)', 'output/pyromancies.csv', ['name', 'description'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')
