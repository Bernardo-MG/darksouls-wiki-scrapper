# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests
from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import NameListScrapper


class WeaponTypePieceScrapper(object):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self):
        super(WeaponTypePieceScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Type
        weapon_type = dom.select('div[data-source="weapon-type"] div')
        if weapon_type:
            weapon_type = weapon_type[0].get_text()
        else:
            weapon_type = ''

        return {'weapon': name, 'type': weapon_type}


class WeaponTypePiecesScrapper(CsvScrapper):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self, root_url):
        super(WeaponTypePiecesScrapper, self).__init__(root_url + '/wiki/Weapons_(Dark_Souls)',
                                                     'output/weapons_weapon_types.csv',
                                                     ['weapon', 'type'])
        self.inner_parser = ListScrapper(root_url, WeaponTypePieceScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list