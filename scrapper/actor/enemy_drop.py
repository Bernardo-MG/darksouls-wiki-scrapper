# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
from scrapper.modules import AsideDropScrapper


class EnemyDropScrapper(CsvScrapper):
    """
    Armor set scrapper.
    """

    def __init__(self, root_url):
        super(EnemyDropScrapper, self).__init__(root_url + '/wiki/Category:Dark_Souls:_Enemies', 'output/enemy_drop.csv',
                                               ['actor', 'location'])
        self.root_url = root_url
        self.inner_parser = ListScrapper(root_url, AsideDropScrapper(), lambda dom: self._extract_links(dom))

    def _extract_links(self, dom):
        result = dom.select('li a.category-page__member-link')

        return list(filter(lambda item: not 'Thread:' in item['title'], result))