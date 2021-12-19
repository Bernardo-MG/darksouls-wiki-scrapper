# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper
from scrapper.modules import NameListScrapper


class WeaponTypeListScrapper(CsvScrapper):
    """
    Weapon type scrapper.
    """

    def __init__(self, root_url):
        super(WeaponTypeListScrapper, self).__init__(root_url + '/wiki/Weapon_Types_(Dark_Souls)', 'output/weapons.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('dt a')