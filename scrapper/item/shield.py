# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper

from scrapper.item.weapon import StatsScrapper


class ShieldScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self):
        super(ShieldScrapper, self).__init__('https://darksouls.fandom.com/wiki/Shields', 'output/shields.csv',
                                             ['name', 'type', 'description', 'weight', 'durability', 'attacks',
                                              'strength_requirement', 'dexterity_requirement', 'intelligence_requirement', 'faith_requirement',
                                              'strength_bonus', 'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                              'physical_damage', 'magic_damage', 'fire_damage', 'lightning_damage',
                                              'critical_damage', 'physical_reduction', 'magic_reduction', 'fire_reduction',
                                              'lightning_reduction', 'stability']
                                             )
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')
