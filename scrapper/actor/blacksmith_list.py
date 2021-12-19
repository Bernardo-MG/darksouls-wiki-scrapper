# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class BlacksmithListScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(BlacksmithListScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Blacksmiths', 'output/blacksmiths.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
