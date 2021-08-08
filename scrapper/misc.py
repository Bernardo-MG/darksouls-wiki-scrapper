# -*- coding: utf-8 -*-

import logging
import os
from scrapper.base import BaseListScrapper
import requests
from bs4 import BeautifulSoup
import re

"""
Relationships scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'

logger = logging.getLogger(os.path.basename(__file__))


class DialogueScrapper(BaseListScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root):
        super(DialogueScrapper, self).__init__(root, '/wiki/Category:Dark_Souls:_Characters', 'output/dialogues.csv',
                                               ['person', 'condition', 'exchange'])

    def scrap_inner_page(self, sub_url):
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

    def extract_list_links(self, dom):
        return dom.select('li a.category-page__member-link')
