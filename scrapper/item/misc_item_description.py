# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class MiscellaneousItemDescriptionScrapper(CsvScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self):
        super(MiscellaneousItemDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Miscellaneous_Items', 'output/misc_items.csv', ['name', 'description'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', DescriptionScrapper(), lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))
