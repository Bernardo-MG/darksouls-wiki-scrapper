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

    def _selectText(self, dom, selector):
        value = dom.select(selector)
        if len(value) > 0:
            value = value[0].get_text()
            if value == '-':
                value = ''
        else:
            value = ''

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

        # Bonus
        strength_bonus = self._selectText(dom, 'div.page.has-right-rail aside td[data-source="str-bonus"]')
        dexterity_bonus = self._selectText(dom, 'div.page.has-right-rail aside td[data-source="dex-bonus"]')
        intelligence_bonus = self._selectText(dom, 'div.page.has-right-rail aside td[data-source="int-bonus"]')
        faith_bonus = self._selectText(dom, 'div.page.has-right-rail aside td[data-source="fth-bonus"]')

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'type': type_name, 'description': description, 'weight': weight, 'durability': durability,
                'attacks': attacks, 'strength_requirement': strength, 'dexterity_requirement': dexterity, 'intelligence_requirement': intelligence,
                'faith_requirement': faith, 'strength_bonus': strength_bonus, 'dexterity_bonus': dexterity_bonus,
                'intelligence_bonus': intelligence_bonus, 'faith_bonus': faith_bonus,
                'physical_reduction': physical_reduction, 'magic_reduction': magic_reduction,
                'fire_reduction': fire_reduction, 'lightning_reduction': lightning_reduction, 'stability': stability,
                'physical_damage': physical, 'magic_damage': magic, 'fire_damage': fire, 'lightning_damage': lightning,
                'critical_damage': critical}


class WeaponScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self):
        super(WeaponScrapper, self).__init__('https://darksouls.fandom.com/wiki/Weapons_(Dark_Souls)', 'output/weapons.csv',
                                             ['name', 'type', 'description', 'weight', 'durability', 'attacks',
                                              'strength_requirement', 'dexterity_requirement', 'intelligence_requirement', 'faith_requirement',
                                              'strength_bonus', 'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                              'physical_damage', 'magic_damage', 'fire_damage', 'lightning_damage',
                                              'critical_damage', 'physical_reduction', 'magic_reduction', 'fire_reduction',
                                              'lightning_reduction', 'stability']
                                             )
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
