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

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        baseName = dom.select('h1#firstHeading')[0].get_text().strip()

        # Poise
        poiseData = dom.select('div.page.has-right-rail table.infobox2 tr:nth-of-type(10) td:nth-of-type(1)')
        if len(poiseData) > 0:
            poise = poiseData[0].get_text()
        else:
            poise = '0'

        # Stats
        stats = []
        stats_rows = dom.select('h2:has(span[id="Upgrades"]) + p + table tr:has(> td)')
        for row in stats_rows:
            cells = row.select('td')
            cells = list(map(lambda cell: cell.contents[0], cells))

            cols = ['name', 'regular', 'strike', 'slash', 'thrust', 'magic', 'fire', 'lightning', 'bleed', 'poison',
                    'curse']

            cells_itr = iter(cells)

            row_stats = {}

            for col in cols:
                value = next(cells_itr, None)
                if value is None or value == '–':
                    row_stats[col] = '0'
                else:
                    row_stats[col] = value

                if col == 'name' and col in row_stats:
                    level = re.search(r'\+\d*', str(row_stats[col]))
                    if level is None:
                        level = '0'
                    else:
                        level = level.group(0)
                    level = level.replace('+', '')
                    row_stats['level'] = level

                    row_stats['name'] = baseName
                row_stats['poise'] = poise

            stats.append(row_stats)

        return stats


class ArmorLevelsScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self):
        super(ArmorLevelsScrapper, self).__init__('https://darksouls.fandom.com/wiki/Category:Dark_Souls:_Armor', 'output/armor_levels.csv',
                                                  ['name', 'level', 'regular', 'strike', 'slash', 'thrust', 'magic',
                                                   'fire', 'lightning', 'bleed', 'poison', 'curse', 'poise'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', LevelsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('a.category-page__member-link')
