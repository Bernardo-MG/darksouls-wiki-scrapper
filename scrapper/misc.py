# -*- coding: utf-8 -*-

from scrapper.base import ListScrapper, CsvScrapper
import requests
from bs4 import BeautifulSoup
import re

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


class DialogueListScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(DialogueListScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Characters', 'output/dialogues.csv',
                                               ['person', 'condition', 'exchange'])
        self.root_url = root_url
        self.list_scrapper = ListScrapper(root_url, DialogueScrapper(), lambda dom: self._extract_links(dom))

    def _transform(self, dom):
        return self.list_scrapper.scrap(dom)

    def _extract_links(self, dom):
        return dom.select('li a.category-page__member-link')
