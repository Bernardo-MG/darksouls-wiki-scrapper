# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging
import re


class StatsScrapper(object):

    def __init__(self):
        super(StatsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Set
        set_name = dom.select('div#content div.mw-parser-output p:nth-of-type(1)')[0].get_text()
        set_name = re.search(r'part of the (.*) Set', set_name)
        if set_name is None:
            set_name = ''
        else:
            set_name = set_name.group(1)

        # Weight
        weight = dom.select('div.page.has-right-rail table.infobox2 tr:nth-of-type(11) td:nth-of-type(1)')[0].get_text()

        # Durability
        durability = dom.select('div.page.has-right-rail table.infobox2 tr:nth-of-type(12) td:nth-of-type(1)')[0].get_text()

        # Type
        type_name = dom.select('div.page.has-right-rail table.infobox2 tr:nth-of-type(13) td:nth-of-type(1)')[0].get_text()

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'set': set_name, 'description': description, 'weight': weight, 'durability': durability, 'type': type_name}


class ArmorDescriptionScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self):
        super(ArmorDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Armor_(Dark_Souls)', 'output/armors.csv',
                                                       ['name', 'set', 'description', 'weight', 'durability', 'type'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('table:not(:nth-of-type(1)) li a')