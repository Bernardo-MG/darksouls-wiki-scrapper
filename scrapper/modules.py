# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging
import re


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

