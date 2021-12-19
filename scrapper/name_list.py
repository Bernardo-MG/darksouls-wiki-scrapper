# -*- coding: utf-8 -*-

from abc import abstractmethod

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class EnemyScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(EnemyScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Enemies', 'output/enemies.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class MerchantScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(MerchantScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Merchants', 'output/merchants.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class BlacksmithScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(BlacksmithScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Blacksmiths', 'output/blacksmiths.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class PhantomScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(PhantomScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Phantoms', 'output/phantoms.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
