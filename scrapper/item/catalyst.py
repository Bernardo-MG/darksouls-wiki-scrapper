# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging


class StatsScrapper(object):

    def __init__(self):
        super(StatsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _selectValue(self, dom, selector):
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

        weight = ''
        durability = ''
        attacks = ''
        for cell in data_cells:
            label = cell.select('.pi-data-label')[0].get_text()
            value = cell.select('.pi-data-value')[0].get_text()
            if label.lower() == 'weight':
                weight = value
            elif label.lower() == 'durability':
                durability = value
            elif label.lower() == 'attack type':
                attacks = value.replace(' / ', '|')

        if weight == '-':
            weight = '0'
        if durability == '-':
            durability = '0'
        if attacks == '-':
            attacks = ''

        # Damage
        physical = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="atk-physical"]')
        magic = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="atk-magic"]')
        fire = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="atk-fire"]')
        lightning = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="atk-lightning"]')
        critical = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="critical"]')

        # Defense
        physical_reduction = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="res-physical"]')
        magic_reduction = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="res-magic"]')
        fire_reduction = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="res-fire"]')
        lightning_reduction = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="res-lightning"]')
        stability = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="stability"]')

        # Requirements
        strength = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="str-req"]')
        dexterity = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="dex-req"]')
        intelligence = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="int-req"]')
        faith = self._selectValue(dom, 'div.page.has-right-rail aside td[data-source="fth-req"]')

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'description': description, 'weight': weight, 'durability': durability,
                'attacks': attacks,
                'strength': strength, 'dexterity': dexterity, 'intelligence': intelligence, 'faith': faith,
                'physical_reduction': physical_reduction, 'magic_reduction': magic_reduction, 'fire_reduction': fire_reduction,
                'lightning_reduction': lightning_reduction, 'stability': stability,
                'physical_dmg': physical, 'magic_dmg': magic, 'fire_dmg': fire, 'lightning_dmg': lightning, 'critical_dmg': critical}


class CatalystDescriptionScrapper(CsvScrapper):
    """
    Catalyst list scrapper.
    """

    def __init__(self, root_url):
        super(CatalystDescriptionScrapper, self).__init__(root_url + '/wiki/Catalysts', 'output/catalysts.csv',
                                                          ['name', 'description', 'weight', 'durability', 'attacks',
                                                           'strength', 'dexterity', 'intelligence', 'faith',
                                                           'physical_dmg', 'magic_dmg', 'fire_dmg', 'lightning_dmg', 'critical_dmg',
                                                           'physical_reduction', 'magic_reduction', 'fire_reduction',
                                                           'lightning_reduction', 'stability'])
        self.inner_parser = ListScrapper(root_url, StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return list(filter(lambda item: not '(damage type)' in item['title'], result))