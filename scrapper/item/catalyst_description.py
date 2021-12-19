# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class CatalystDescriptionScrapper(CsvScrapper):
    """
    Catalyst list scrapper.
    """

    def __init__(self, root_url):
        super(CatalystDescriptionScrapper, self).__init__(root_url + '/wiki/Catalysts', 'output/catalysts.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return list(filter(lambda item: not '(damage type)' in item['title'], result))