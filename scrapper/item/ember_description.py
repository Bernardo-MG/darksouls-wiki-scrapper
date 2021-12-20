# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class EmberDescriptionScrapper(CsvScrapper):
    """
    Ember list scrapper.
    """

    def __init__(self, root_url):
        super(EmberDescriptionScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Embers', 'output/embers.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('li a.category-page__member-link')