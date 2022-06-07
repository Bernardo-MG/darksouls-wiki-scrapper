# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging


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