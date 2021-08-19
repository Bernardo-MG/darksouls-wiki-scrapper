# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from scrapper.base import CsvScrapper


class BaseNameListScrapper(CsvScrapper):
    """
    Scrapper for name list pages. Will find all the names in a page and store them in a list.
    """

    def __init__(self, root_url, list_page, output_file):
        super(BaseNameListScrapper, self).__init__(root_url + list_page, output_file, ['name'])

    def scrap_data(self, dom):
        main_list = self.extract_list(dom)

        return list(map(lambda item: {'name': item.get_text()}, main_list))

    @abstractmethod
    def extract_list(self, dom):
        """
        Extracts the list of names from the DOM.

        Returns
        -------
        list
            a list of text elements
        """
        pass


class ArmorSetScrapper(BaseNameListScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root):
        super(ArmorSetScrapper, self).__init__(root, '/wiki/Armor_(Dark_Souls)', 'output/armor_sets.csv')

    def extract_list(self, dom):
        return dom.select('div[title="Sets"] li a')


class ShieldTypeScrapper(BaseNameListScrapper):
    """
    Shield type scrapper.
    """

    def __init__(self, root):
        super(ShieldTypeScrapper, self).__init__(root, '/wiki/Shields', 'output/shield_types.csv')

    def extract_list(self, dom):
        return dom.select('dt a')


class WeaponTypeScrapper(BaseNameListScrapper):
    """
    Weapon type scrapper.
    """

    def __init__(self, root):
        super(WeaponTypeScrapper, self).__init__(root, '/wiki/Weapon_Types_(Dark_Souls)', 'output/weapon_types.csv')

    def extract_list(self, dom):
        return dom.select('dt a')


class UniqueWeaponScrapper(BaseNameListScrapper):
    """
    Unique weapon scrapper.
    """

    def __init__(self, root):
        super(UniqueWeaponScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Unique_Weapons', 'output/unique_weapons.csv')

    def extract_list(self, dom):
        return dom.select('ul.category-page__members-for-char li a.category-page__member-link')
