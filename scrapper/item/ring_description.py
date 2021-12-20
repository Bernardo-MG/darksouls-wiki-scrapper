# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class RingDescriptionScrapper(CsvScrapper):
    """
    Ring list scrapper.
    """

    def __init__(self, root_url):
        super(RingDescriptionScrapper, self).__init__(root_url + '/wiki/Rings_(Dark_Souls)', 'output/rings.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')
