# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class RingDescriptionScrapper(CsvScrapper):
    """
    Ring list scrapper.
    """

    def __init__(self):
        super(RingDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Rings_(Dark_Souls)', 'output/rings.csv', ['name', 'description'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', DescriptionScrapper(), lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')
