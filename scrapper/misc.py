# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
from scrapper.modules import DialogueScrapper, AsideLocationScrapper, LocationScrapper, AsideDropScrapper, \
    AdjacentLocationScrapper

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class DialogueListScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(DialogueListScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Characters', 'output/dialogues.csv',
                                               ['person', 'condition', 'exchange'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, DialogueScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('li a.category-page__member-link')


class EnemyLocationScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(EnemyLocationScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Enemies', 'output/enemy_locations.csv',
                                               ['actor', 'location'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, AsideLocationScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class CharacterLocationScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(CharacterLocationScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Characters', 'output/character_locations.csv',
                                               ['actor', 'location'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, LocationScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class EnemyDropScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(EnemyDropScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Enemies', 'output/enemy_drop.csv',
                                               ['actor', 'location'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, AsideDropScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))


class AdjacentLocationsScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(AdjacentLocationsScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Locations', 'output/adjacent_locations.csv',
                                               ['location', 'adjacent'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, AdjacentLocationScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))

