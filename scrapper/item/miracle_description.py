# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class MiracleDescriptionScrapper(CsvScrapper):
    """
    Miracle list scrapper.
    """

    def __init__(self, root_url):
        super(MiracleDescriptionScrapper, self).__init__(root_url + '/wiki/Miracle_(Dark_Souls)', 'output/miracles.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')