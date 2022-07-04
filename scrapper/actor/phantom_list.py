# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class PhantomListScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self):
        super(PhantomListScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Phantoms', 'output/phantoms.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
