# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class ShieldTypeListScrapper(CsvScrapper):
    """
    Shield type scrapper.
    """

    def __init__(self, root_url):
        super(ShieldTypeListScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shield_types.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('dt a')