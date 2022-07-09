# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.item.weapon_levels import LevelsScrapper


class ShieldLevelsScrapper(CsvScrapper):
    """
    Weapon list scrapper.
    """

    def __init__(self):
        super(ShieldLevelsScrapper, self).__init__('https://darksouls.fandom.com/wiki/Shields', 'output/shield_levels.csv',
                                                   ['name', 'path', 'level', 'physical_damage', 'magic_damage',
                                                    'fire_damage', 'lightning_damage', 'strength_bonus',
                                                    'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                                    'physical_reduction', 'magic_reduction', 'fire_reduction',
                                                    'lightning_reduction', 'critical', 'stability'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', LevelsScrapper(), lambda dom: self._extract_links(dom))

    @staticmethod
    def _extract_links(dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')
