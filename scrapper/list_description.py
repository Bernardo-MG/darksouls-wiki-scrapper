# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from scrapper.base import CsvScrapper, ListScrapper
import logging


class DescriptionScrapper(object):
    """
    Scrapper for pages with description.
    """

    def __init__(self):
        super(DescriptionScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'description': description}


class AmmunitionScrapper(CsvScrapper):
    """
    Ammunition list scrapper.
    """

    def __init__(self, root_url):
        super(AmmunitionScrapper, self).__init__(root_url + '/wiki/Ammunition', 'output/ammunition.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('td:nth-of-type(1) a:has(> img)')


class ArmorScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ArmorScrapper, self).__init__(root_url + '/wiki/Armor_(Dark_Souls)', 'output/armors.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('table:not(:nth-of-type(1)) li a')


class CatalystScrapper(CsvScrapper):
    """
    Catalyst list scrapper.
    """

    def __init__(self, root_url):
        super(CatalystScrapper, self).__init__(root_url + '/wiki/Catalysts', 'output/catalysts.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return list(filter(lambda item: not '(damage type)' in item['title'], result))


class EmberScrapper(CsvScrapper):
    """
    Ember list scrapper.
    """

    def __init__(self, root_url):
        super(EmberScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Embers', 'output/embers.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('li a.category-page__member-link')


class KeyItemScrapper(CsvScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self, root_url):
        super(KeyItemScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Key_Items', 'output/key_items.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))


class MiracleScrapper(CsvScrapper):
    """
    Miracle list scrapper.
    """

    def __init__(self, root_url):
        super(MiracleScrapper, self).__init__(root_url + '/wiki/Miracle_(Dark_Souls)', 'output/miracles.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class MiscellaneousItemScrapper(CsvScrapper):
    """
    Key item list scrapper.
    """

    def __init__(self, root_url):
        super(MiscellaneousItemScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Miscellaneous_Items', 'output/misc_items.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))


class PyromancyScrapper(CsvScrapper):
    """
    Pyromancy list scrapper.
    """

    def __init__(self, root_url):
        super(PyromancyScrapper, self).__init__(root_url + '/wiki/Pyromancy_(Dark_Souls)', 'output/pyromancies.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class RingScrapper(CsvScrapper):
    """
    Ring list scrapper.
    """

    def __init__(self, root_url):
        super(RingScrapper, self).__init__(root_url + '/wiki/Rings_(Dark_Souls)', 'output/rings.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class ShieldScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ShieldScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shields.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')


class SorceryScrapper(CsvScrapper):
    """
    Sorcery list scrapper.
    """

    def __init__(self, root_url):
        super(SorceryScrapper, self).__init__(root_url + '/wiki/Sorcery_(Dark_Souls)', 'output/sorceries.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('.article-table td:nth-of-type(1) a:has(> img)')


class SoulScrapper(CsvScrapper):
    """
    Soul list scrapper.
    """

    def __init__(self, root_url):
        super(SoulScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Souls', 'output/souls.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))


class TalismanScrapper(CsvScrapper):
    """
    Talisman list scrapper.
    """

    def __init__(self, root_url):
        super(TalismanScrapper, self).__init__(root_url + '/wiki/Talismans', 'output/talismans.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return list(filter(lambda item: not '(damage type)' in item['title'], result))


class UpgradeMaterialScrapper(CsvScrapper):
    """
    Upgrade material list scrapper.
    """

    def __init__(self, root_url):
        super(UpgradeMaterialScrapper, self).__init__(root_url + '/wiki/Upgrade_Materials', 'output/talismans.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('span.mw-headline a')


class WeaponScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root_url):
        super(WeaponScrapper, self).__init__(root_url + '/wiki/Upgrade_Materials', 'output/talismans.csv', ['name', 'description'])
        self.inner_parser = ListScrapper(root_url, DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
