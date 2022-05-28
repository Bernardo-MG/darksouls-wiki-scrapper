# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging


class StatsScrapper(object):

    def __init__(self):
        super(StatsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Data
        data_cells = dom.select('div.page.has-right-rail aside div.pi-data')

        weight = ''
        durability = ''
        type_name = ''
        attacks = ''
        for cell in data_cells:
            label = cell.select('.pi-data-label')[0].get_text()
            value = cell.select('.pi-data-value')[0].get_text()
            if label.lower() == 'weight':
                weight = value
            elif label.lower() == 'durability':
                durability = value
            elif label.lower() == 'weapon type':
                type_name = value
            elif label.lower() == 'attack type':
                attacks = value.replace(' / ', '|')

        if weight == '-':
            weight = '0'
        if durability == '-':
            durability = '0'
        if attacks == '-':
            attacks = ''

        # Requirements
        strength = dom.select('div.page.has-right-rail aside td[data-source="str-req"]')
        if len(strength) > 0:
            strength = strength[0].get_text()
            if strength == '-':
                strength = '0'
        else:
            strength = '0'
        dexterity = dom.select('div.page.has-right-rail aside td[data-source="dex-req"]')
        if len(dexterity) > 0:
            dexterity = dexterity[0].get_text()
            if dexterity == '-':
                dexterity = '0'
        else:
            dexterity = '0'
        intelligence = dom.select('div.page.has-right-rail aside td[data-source="int-req"]')
        if len(intelligence) > 0:
            intelligence = intelligence[0].get_text()
            if intelligence == '-':
                intelligence = '0'
        else:
            intelligence = '0'
        faith = dom.select('div.page.has-right-rail aside td[data-source="fth-req"]')
        self.logger.debug("Faith: %s", faith);
        if len(faith) > 0:
            faith = faith[0].get_text()
            if faith == '-':
                faith = '0'
        else:
            faith = '0'

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'type': type_name, 'description': description, 'weight': weight, 'durability': durability,
                'attacks': attacks, 'strength': strength, 'dexterity': dexterity, 'intelligence': intelligence,
                'faith': faith}


class ShieldScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ShieldScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shields.csv',
                                             ['name', 'type', 'description', 'weight', 'durability', 'attacks',
                                                         'strength', 'dexterity', 'intelligence', 'faith'])
        self.inner_parser = ListScrapper(root_url, StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')
