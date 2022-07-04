# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import DescriptionScrapper


class UpgradeMaterialDescriptionScrapper(CsvScrapper):
    """
    Upgrade material list scrapper.
    """

    def __init__(self):
        super(UpgradeMaterialDescriptionScrapper, self).__init__('https://darksouls.fandom.com/wiki/Upgrade_Materials', 'output/upgrade_materials.csv', ['name', 'description'])
        self.inner_parser = ListScrapper('https://darksouls.fandom.com', DescriptionScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        return dom.select('span.mw-headline a')
