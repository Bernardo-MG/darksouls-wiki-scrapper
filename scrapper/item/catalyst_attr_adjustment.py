# -*- coding: utf-8 -*-

from scrapper.base import CsvScrapper, ListScrapper
import requests
from bs4 import BeautifulSoup
import logging

from scrapper.item.weapon import StatsScrapper


class AdjustmentScrapper(object):

    def __init__(self):
        super(AdjustmentScrapper, self).__init__()

    @staticmethod
    def scrap(dom):
        headers = dom.select('table.wiki_table tr:nth-child(2) th')
        headers = list(headers)
        headers_count = len(headers)

        attr = dom.select('table.wiki_table td:nth-child(1)')
        attr = list(map(lambda c: c.get_text(), attr))
        attr.pop(0)
        attr.pop(0)
        attr_count = len(attr)

        result = []
        for i in range(1, headers_count):
            name = headers[i].get_text()
            name = name.strip(' ∗*')
            values = dom.select('table.wiki_table td:nth-child(%d)' % (i + 1))
            values = list(map(lambda c: c.get_text(), values))
            for j in range(1, attr_count):
                result.append({'name': name, 'intelligence': attr[j], 'adjustment': values[j]})

        return result


class CatalystAttributeAdjustmentScrapper(CsvScrapper):
    """
    Talisman list scrapper.
    """

    def __init__(self):
        super(CatalystAttributeAdjustmentScrapper, self).__init__(
            'https://darksouls.wiki.fextralife.com/Int-Faith+Catalyst+Magic+Adjustment+Values',
            'output/catalyst_adjustments.csv',
            ['name', 'intelligence', 'adjustment']
        )
        self.inner_parser = AdjustmentScrapper()