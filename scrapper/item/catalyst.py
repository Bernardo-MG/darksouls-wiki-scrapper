# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging

from scrapper.item.weapon import StatsScrapper


class CatalystScrapper(CsvScrapper):
    """
    Catalyst list scrapper.
    """

    def __init__(self, root_url):
        super(CatalystScrapper, self).__init__(root_url + '/wiki/Catalysts', 'output/catalysts.csv',
                                             ['name', 'type', 'description', 'weight', 'durability', 'attacks',
                                              'strength_requirement', 'dexterity_requirement', 'intelligence_requirement', 'faith_requirement',
                                              'strength_bonus', 'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                              'physical_damage', 'magic_damage', 'fire_damage', 'lightning_damage',
                                              'critical_damage', 'physical_reduction', 'magic_reduction', 'fire_reduction',
                                              'lightning_reduction', 'stability']
                                               )
        self.inner_parser = ListScrapper(root_url, StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('td:nth-of-type(1) a:has(> img)')

        return list(filter(lambda item: not '(damage type)' in item['title'], result))
