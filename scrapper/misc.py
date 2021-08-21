# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
import requests
from bs4 import BeautifulSoup
import re
import logging

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class DialogueScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(DialogueScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Dialogue
        exchanges = dom.select('h2:has(span[id="Dialogue"]) + table tr')

        dialogue = []
        for exchange in exchanges:
            data = exchange.select('td')
            if len(data) == 2:

                condition = data[0].get_text()
                condition = re.sub(r'\n', '', condition)

                exchange = data[1].get_text()
                exchange = re.sub(r'\n', '', exchange)

                dialogue.append({'person': name,
                                 'condition': condition,
                                 'exchange': exchange})

        return dialogue


class AsideDropScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(AsideDropScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        drops = dom.select('aside[role="region"] div[data-source="drops"] a')
        drops = list(filter(lambda item: not 'None' == item['title'], drops))

        return list(map(lambda location: {'actor': name, 'location': location['title']}, drops))


class AsideLocationScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(AsideLocationScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        locations = dom.select('aside[role="region"] div[data-source="location"] a')

        return list(map(lambda location: {'actor': name, 'location': location['title']}, locations))


class LocationScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(LocationScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        locations = dom.select('h2:nth-of-type(1) + p > a[title]')

        return list(map(lambda location: {'actor': name, 'location': location['title']}, locations))


class AdjacentLocationScrapper(object):
    """
    Dialogue scrapper.
    """

    def __init__(self):
        super(AdjacentLocationScrapper, self).__init__()

    def scrap(self, sub_url):
        html = requests.get(sub_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Locations
        locations = dom.select('h2:has(> span#Adjacent_locations) + ul a[title]')

        return list(map(lambda location: {'location': name, 'adjacent': location['title']}, locations))


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

