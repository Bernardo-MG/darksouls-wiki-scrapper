# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class UniqueWeaponScrapper(CsvScrapper):
    """
    Unique weapon scrapper.
    """

    def __init__(self):
        super(UniqueWeaponScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Unique_Weapons', 'output/unique_weapons.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('ul.category-page__members-for-char li a.category-page__member-link')