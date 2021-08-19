# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
import requests
from bs4 import BeautifulSoup

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class ArmorSetRelScrapper(object):
    """
    Armor set relationships scrapper.
    """

    def __init__(self):
        super(ArmorSetRelScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Set
        set_name = dom.select('h1#firstHeading')[0].get_text()

        # Pieces
        pieces_list = dom.select('h2:has(span[id="set_pieces" i]) + ul a')
        pieces = list(map(lambda item: item['title'], pieces_list))

        data = []
        for piece in pieces:
            data.append({'armor': piece, 'set':set_name})

        return data


class ShieldTypeRelScrapper(object):
    """
    Shield type relationships scrapper.
    """

    def __init__(self):
        super(ShieldTypeRelScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Type
        shield_type = dom.select('div[data-source="weapon-type"] div')[0].get_text()

        return {'shield': name, 'type': shield_type}


class WeaponTypeRelScrapper(object):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self, root):
        super(WeaponTypeRelScrapper, self).__init__()

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


class ArmorSetRelsScrapper(CsvScrapper):
    """
    Armor set relationships scrapper.
    """

    def __init__(self, root_url):
        super(ArmorSetRelsScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)',
                                                     'output/armors_armor_sets.csv',
                                                     ['armor', 'set'])
        self.list_scrapper = ListScrapper(root_url, ArmorSetRelScrapper(), lambda dom: self._extract_links(dom))

    def _transform(self, dom):
        return self.list_scrapper.scrap(dom)

    def _extract_links(self, dom):
        return dom.select('div[title="Sets"] li a')


class ShieldTypeRelsScrapper(CsvScrapper):
    """
    Shield type relationships scrapper.
    """

    def __init__(self, root_url):
        super(ShieldTypeRelsScrapper, self).__init__(root_url + '/wiki/Shields',
                                                     'output/shields_shield_types.csv',
                                                     ['shield', 'type'])
        self.list_scrapper = ListScrapper(root_url, ShieldTypeRelScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')


class WeaponTypeRelsScrapper(CsvScrapper):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self, root_url):
        super(WeaponTypeRelsScrapper, self).__init__(root_url + '/wiki/Weapons_(Dark_Souls)',
                                                     'output/weapons_weapon_types.csv',
                                                     ['weapon', 'type'])
        self.list_scrapper = ListScrapper(root_url, WeaponTypeRelScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
