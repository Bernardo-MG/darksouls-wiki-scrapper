# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class WeaponDescriptionScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root_url):
        super(WeaponDescriptionScrapper, self).__init__(root_url + '/wiki/Weapons_(Dark_Souls)', 'output/weapons.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
