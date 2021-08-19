# -*- coding: utf-8 -*-

from abc import abstractmethod

from scrapper.base import CsvScrapper


class NameListScrapper(object):
    """
    Scrapper for name list pages. Will find all the names in a page and store them in a list.
    """

    def __init__(self, _extract_links):
        super(NameListScrapper, self).__init__()
        self._extract_links = _extract_links

    def scrap(self, dom):
        main_list = self._extract_links(dom)

        return list(map(lambda item: {'name': item.get_text()}, main_list))


class BaseNameListScrapper(CsvScrapper):
    """
    Scrapper for name list pages. Will find all the names in a page and store them in a list.
    """

    def __init__(self, root_url, list_page, output_file):
        super(BaseNameListScrapper, self).__init__(root_url + list_page, output_file, ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    @abstractmethod
    def _extract_links(self, dom):
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

    def _extract_links(self, dom):
        return dom.select('div[title="Sets"] li a')


class ShieldTypeScrapper(BaseNameListScrapper):
    """
    Shield type scrapper.
    """

    def __init__(self, root):
        super(ShieldTypeScrapper, self).__init__(root, '/wiki/Shields', 'output/shield_types.csv')

    def _extract_links(self, dom):
        return dom.select('dt a')


class WeaponTypeScrapper(BaseNameListScrapper):
    """
    Weapon type scrapper.
    """

    def __init__(self, root):
        super(WeaponTypeScrapper, self).__init__(root, '/wiki/Weapon_Types_(Dark_Souls)', 'output/weapon_types.csv')

    def _extract_links(self, dom):
        return dom.select('dt a')


class UniqueWeaponScrapper(BaseNameListScrapper):
    """
    Unique weapon scrapper.
    """

    def __init__(self, root):
        super(UniqueWeaponScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Unique_Weapons', 'output/unique_weapons.csv')

    def _extract_links(self, dom):
        return dom.select('ul.category-page__members-for-char li a.category-page__member-link')


class EnemyScrapper(BaseNameListScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root):
        super(EnemyScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Enemies', 'output/enemies.csv')

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return filter(lambda item: not 'Thread:' in item['title'], result)
