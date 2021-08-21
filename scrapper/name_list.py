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


class ArmorSetScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(ArmorSetScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)', 'output/armor_sets.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('table:nth-of-type(1) li a')


class ShieldTypeScrapper(CsvScrapper):
    """
    Shield type scrapper.
    """

    def __init__(self, root_url):
        super(ShieldTypeScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shield_types.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('dt a')


class WeaponTypeScrapper(CsvScrapper):
    """
    Weapon type scrapper.
    """

    def __init__(self, root_url):
        super(WeaponTypeScrapper, self).__init__(root_url + '/wiki/Weapon_Types_(Dark_Souls)', 'output/weapons.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('dt a')


class UniqueWeaponScrapper(CsvScrapper):
    """
    Unique weapon scrapper.
    """

    def __init__(self, root_url):
        super(UniqueWeaponScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Unique_Weapons', 'output/unique_weapons.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        return dom.select('ul.category-page__members-for-char li a.category-page__member-link')


class EnemyScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(EnemyScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Enemies', 'output/enemies.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class MerchantScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(MerchantScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Merchants', 'output/merchants.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class BlacksmithScrapper(CsvScrapper):
    """
    Enemy list scrapper.
    """

    def __init__(self, root_url):
        super(BlacksmithScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Blacksmiths', 'output/blacksmiths.csv', ['name'])
        self.inner_parser = NameListScrapper(self._extract_links)

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))
