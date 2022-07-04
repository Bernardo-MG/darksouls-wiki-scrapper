# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging


class StatsScrapper(object):

    def __init__(self):
        super(StatsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _select_value(self, dom, selector):
        value = dom.select(selector)
        if len(value) > 0:
            value = value[0].get_text()
            if value == '-':
                value = '0'
        else:
            value = '0'

        return value

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Data
        data_cells = dom.select('div.page.has-right-rail aside div.pi-data')

        type_name = ''
        slots = ''
        uses = ''
        for cell in data_cells:
            label = cell.select('.pi-data-label')
            value = cell.select('.pi-data-value')
            if len(label) > 0 and len(value) > 0:
                label = label[0].get_text()
                value = value[0].get_text()
                if label.lower() == 'magic type':
                    type_name = value
                elif label.lower() == 'slots':
                    slots = value
                elif label.lower() == 'uses':
                    uses = value

        # Requirements
        intelligence = self._select_value(dom, 'div[data-source="int-req"] .pi-data-value')
        faith = self._select_value(dom, 'div[data-source="fth-req"] .pi-data-value')

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'school': type_name, 'description': description,
                'intelligence': intelligence, 'faith': faith,
                'slots': slots, 'uses': uses}


class MagicScrapper(CsvScrapper):
    """
    Miracle list scrapper.
    """

    def __init__(self):
        super(MagicScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Magic', 'output/spells.csv',
                                                         ['name', 'school', 'description', 'intelligence', 'faith',
                                                          'slots', 'uses'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', StatsScrapper(), lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Category:' in item['title'], result))