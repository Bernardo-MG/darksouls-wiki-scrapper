# -*- coding: utf-8 -*-

from scrapper.base import BaseListScrapper
import requests
from bs4 import BeautifulSoup

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class ArmorSetRelsScrapper(BaseListScrapper):
    """
    Armor set relationships scrapper.
    """

    def __init__(self, root):
        super(ArmorSetRelsScrapper, self).__init__(root, '/wiki/Armor_(Dark_Souls)',
                                                     'output/armors_armor_sets.csv',
                                                     ['armor', 'set'])

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Set
        type = dom.select('h1#firstHeading')[0].get_text()

        # Pieces
        pieces_list = dom.select('h2:has(span[id="set_pieces" i]) + ul a')
        pieces = list(map(lambda item: item['title'], pieces_list))

        data = []
        for piece in pieces:
            data.append({'armor': piece, 'set':type})

        return data

    def _extract_links(self, dom):
        return dom.select('div[title="Sets"] li a')


class ShieldTypeRelsScrapper(BaseListScrapper):
    """
    Shield type relationships scrapper.
    """

    def __init__(self, root):
        super(ShieldTypeRelsScrapper, self).__init__(root, '/wiki/Shields',
                                                     'output/shields_shield_types.csv',
                                                     ['shield', 'type'])

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Type
        type = dom.select('div[data-source="weapon-type"] div')[0].get_text()

        return {'shield': name, 'type': type}

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')


class WeaponTypeRelsScrapper(BaseListScrapper):
    """
    Weapon type relationships scrapper.
    """

    def __init__(self, root):
        super(WeaponTypeRelsScrapper, self).__init__(root, '/wiki/Weapons_(Dark_Souls)',
                                                     'output/weapons_weapon_types.csv',
                                                     ['weapon', 'type'])

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Type
        type = dom.select('div[data-source="weapon-type"] div')
        if type:
            type = type[0].get_text()
        else:
            type = ''

        return {'weapon': name, 'type': type}

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
