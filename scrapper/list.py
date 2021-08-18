# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from scrapper.base import BaseListDescriptionScrapper, BaseListScrapper

"""
Listing scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class AmmunitionScrapper(BaseListDescriptionScrapper):
    """
    Ammunition list scrapper.
    """

    def __init__(self, root):
        super(AmmunitionScrapper, self).__init__(root, '/wiki/Ammunition', 'output/ammunition.csv')

    def extract_list_links(self, dom):
        return dom.select('td:nth-of-type(1) a:has(> img)')


class ArmorScrapper(BaseListDescriptionScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root):
        super(ArmorScrapper, self).__init__(root, '/wiki/Armor_(Dark_Souls)', 'output/armors.csv')

    def extract_list_links(self, dom):
        return dom.select('div[title="Pieces"] li a')


class CatalystScrapper(BaseListDescriptionScrapper):
    """
    Catalyst list scrapper.
    """

    def __init__(self, root):
        super(CatalystScrapper, self).__init__(root, '/wiki/Catalysts', 'output/catalysts.csv')

    def extract_list_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return filter(lambda item: not '(damage type)' in item['title'], result)


class EmberScrapper(BaseListDescriptionScrapper):
    """
    Ember list scrapper.
    """

    def __init__(self, root):
        super(EmberScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Embers', 'output/embers.csv')

    def extract_list_links(self, dom):
        return dom.select('li a.category-page__member-link')


class KeyItemScrapper(BaseListDescriptionScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self, root):
        super(KeyItemScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Key_Items', 'output/key_items.csv')

    def extract_list_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Category:' in item['title'], result)


class MiracleScrapper(BaseListDescriptionScrapper):
    """
    Miracle list scrapper.
    """

    def __init__(self, root):
        super(MiracleScrapper, self).__init__(root, '/wiki/Miracle_(Dark_Souls)', 'output/miracles.csv')

    def extract_list_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class MiscellaneousItemScrapper(BaseListDescriptionScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self, root):
        super(MiscellaneousItemScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Miscellaneous_Items', 'output/misc_items.csv')

    def extract_list_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Category:' in item['title'], result)


class PyromancyScrapper(BaseListDescriptionScrapper):
    """
    Pyromancy list scrapper.
    """

    def __init__(self, root):
        super(PyromancyScrapper, self).__init__(root, '/wiki/Pyromancy_(Dark_Souls)', 'output/pyromancies.csv')

    def extract_list_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class RingScrapper(BaseListDescriptionScrapper):
    """
    Ring list scrapper.
    """

    def __init__(self, root):
        super(RingScrapper, self).__init__(root, '/wiki/Rings_(Dark_Souls)', 'output/rings.csv')

    def extract_list_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class ShieldScrapper(BaseListDescriptionScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root):
        super(ShieldScrapper, self).__init__(root, '/wiki/Shields', 'output/shields.csv')

    def extract_list_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')


class SorceryScrapper(BaseListDescriptionScrapper):
    """
    Sorcery list scrapper.
    """

    def __init__(self, root):
        super(SorceryScrapper, self).__init__(root, '/wiki/Sorcery_(Dark_Souls)', 'output/sorceries.csv')

    def extract_list_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class SoulScrapper(BaseListDescriptionScrapper):
    """
    Soul list scrapper.
    """

    def __init__(self, root):
        super(SoulScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Souls', 'output/souls.csv')

    def extract_list_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Category:' in item['title'], result)


class TalismanScrapper(BaseListDescriptionScrapper):
    """
    Talisman list scrapper.
    """

    def __init__(self, root):
        super(TalismanScrapper, self).__init__(root, '/wiki/Talismans', 'output/talismans.csv')

    def extract_list_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return filter(lambda item: not '(damage type)' in item['title'], result)


class UpgradeMaterialScrapper(BaseListDescriptionScrapper):
    """
    Upgrade material list scrapper.
    """

    def __init__(self, root):
        super(UpgradeMaterialScrapper, self).__init__(root, '/wiki/Upgrade_Materials', 'output/upgrade_materials.csv')

    def extract_list_links(self, dom):
        return dom.select('span.mw-headline a')


class WeaponScrapper(BaseListDescriptionScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root):
        super(WeaponScrapper, self).__init__(root, '/wiki/Weapons_(Dark_Souls)', 'output/weapons.csv')

    def extract_list_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list


class EnemyScrapper(BaseListScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root):
        super(EnemyScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Enemies', 'output/enemies.csv', ['name', 'url'])

    def extract_list_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Thread:' in item['title'], result)

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text().strip()

        return {'name': name, 'url': sub_url}
