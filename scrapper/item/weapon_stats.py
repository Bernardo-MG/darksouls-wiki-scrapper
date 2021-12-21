# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging


class StatsScrapper(object):
    """
    Scrapper for pages with a description.
    """

    def __init__(self):
        super(StatsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Stats
        stats = []
        stats_rows = dom.select('h2:has(span[id="Upgrades"]) + div tr:has(> td)')
        for row in stats_rows:
            cells = row.select('td')
            cells = list(map(lambda cell: cell.contents[0], cells))

            cols = ['name', 'physical', 'magic', 'fire', 'lightning', 'strength', 'dexterity', 'intelligence', 'faith',
                    'physical_reduction', 'magic_reduction', 'fire_reduction', 'lightning_reduction']

            cells_itr = iter(cells)

            row_stats = {}

            for col in cols:
                value = next(cells_itr, None)
                if value is None or value == '–':
                    row_stats[col] = '0'
                else:
                    row_stats[col] = value

            stats.append(row_stats)


        return stats


class WeaponStatsScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self, root_url):
        super(WeaponStatsScrapper, self).__init__(root_url + '/wiki/Weapons_(Dark_Souls)', 'output/weapon_stats.csv',
                                                  ['name', 'physical', 'magic', 'fire', 'lightning', 'strength',
                                                   'dexterity', 'intelligence', 'faith', 'physical_reduction',
                                                   'magic_reduction', 'fire_reduction', 'lightning_reduction'])
        self.inner_parser = ListScrapper(root_url, StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
