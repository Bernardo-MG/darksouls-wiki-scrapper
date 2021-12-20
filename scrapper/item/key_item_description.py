# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class KeyItemDescriptionScrapper(CsvScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self, root_url):
        super(KeyItemDescriptionScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Key_Items', 'output/key_items.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))