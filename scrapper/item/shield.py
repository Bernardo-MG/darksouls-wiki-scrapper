# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper

from scrapper.item.weapon import StatsScrapper


class ShieldScrapper(CsvScrapper):
    """
    Armor list scrapper.
    """

    def __init__(self, root_url):
        super(ShieldScrapper, self).__init__(root_url + '/wiki/Shields', 'output/shields.csv',
                                             ['name', 'type', 'description', 'weight', 'durability', 'attacks',
                                              'strength', 'dexterity', 'intelligence', 'faith',
                                              'strength_bonus', 'dexterity_bonus', 'intelligence_bonus', 'faith_bonus',
                                              'physical_dmg', 'magic_dmg', 'fire_dmg', 'lightning_dmg',
                                              'critical_dmg', 'physical_reduction', 'magic_reduction', 'fire_reduction',
                                              'lightning_reduction', 'stability']
                                             )
        self.inner_parser = ListScrapper(root_url, StatsScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('h2:has(> span#List_of_Shields) + table li a')
