# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging
import re


class LevelsScrapper(object):
    """
    Scrapper for pages with a description.
    """

    def __init__(self):
        super(LevelsScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def scrap(url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        baseName = dom.select('h1#firstHeading')[0].get_text().strip()

        # Static values
        critical = dom.select('div.page.has-right-rail aside td[data-source="critical"]')
        if len(critical) > 0:
            critical = critical[0].get_text()
        else:
            critical = '0'
        stability = dom.select('div.page.has-right-rail aside td[data-source="stability"]')
        if len(stability) > 0:
            stability = stability[0].get_text()
        else:
            stability = '0'

        # Stats
        stats = []
        stats_rows = dom.select('h2:has(span[id="Upgrades"]) + div tr:has(> td)')
        if not stats_rows:
            stats_rows = dom.select('h2:has(span[id="Upgrades"]) + p + table tr:has(> td)')
        for row in stats_rows:
            cells = row.select('td')
            cells = list(map(lambda cell: cell.contents[0], cells))

            cols = ['name', 'physical_damage', 'magic_damage', 'fire_damage', 'lightning_damage', 'strength_bonus',
                    'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                    'physical_reduction', 'magic_reduction', 'fire_reduction', 'lightning_reduction']

            cells_itr = iter(cells)

            row_stats = {}

            for col in cols:
                value = next(cells_itr, None)
                if value is None or value == '–':
                    row_stats[col] = '0'
                else:
                    row_stats[col] = value

                if col == 'name':
                    type = re.sub(' ' + baseName, '', row_stats['name'])
                    type = re.sub(r'\+\d*', '', type)
                    type = type.strip()
                    if type == baseName:
                        type = 'Standard'
                    row_stats['path'] = type

                    level = re.search(r'\+\d*', row_stats['name'])
                    if level is None:
                        level = '0'
                    else:
                        level = level.group(0)
                    level = level.replace('+', '')

                    row_stats['level'] = level
                    row_stats['name'] = baseName
                elif col.endswith("_bonus"):
                    if row_stats[col] == '0':
                        row_stats[col] = ''

            row_stats['critical'] = critical
            row_stats['stability'] = stability
            stats.append(row_stats)

        return stats


class WeaponLevelsScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self):
        super(WeaponLevelsScrapper, self).__init__('https://darksouls.fandom.com/wiki/Weapons_(Dark_Souls)',
                                                   'output/weapon_levels.csv',
                                                   ['name', 'path', 'level', 'physical_damage', 'magic_damage',
                                                    'fire_damage', 'lightning_damage', 'strength_bonus',
                                                    'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                                    'physical_reduction', 'magic_reduction', 'fire_reduction',
                                                    'lightning_reduction', 'critical', 'stability'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', LevelsScrapper(),
                                         lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        main_list = dom.select('h2:has(> span#Weapons) + table li a')
        main_list = main_list + dom.select('h2:has(> span#Weapons) + table + table li a')

        return main_list
