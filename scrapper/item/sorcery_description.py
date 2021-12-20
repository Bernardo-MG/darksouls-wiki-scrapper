# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class SorceryDescriptionScrapper(CsvScrapper):
    """
    Sorcery list scrapper.
    """

    def __init__(self, root_url):
        super(SorceryDescriptionScrapper, self).__init__(root_url + '/wiki/Sorcery_(Dark_Souls)', 'output/sorceries.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')
