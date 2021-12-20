# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

"""
Various modules which take care of small steps of the parsing process.
"""


class DescriptionScrapper(object):
    """
    Scrapper for pages with a description.
    """

    def __init__(self):
        super(DescriptionScrapper, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def scrap(self, url):
        html = requests.get(url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Name
        name = dom.select('h1#firstHeading')[0].get_text()

        # Description
        description = dom.select('div.mainbg dd i')
        info = []
        for item in description:
            if item.contents:
                info.append(item.get_text())

        description = '\\n'.join(info)

        return {'name': name, 'description': description}


class NameListScrapper(object):
    """
    Scrapper for name list pages. Will find all the names in a page and store them in a list.
    """

    def __init__(self, _extract_links):
        super(NameListScrapper, self).__init__()
        self._extract_links = _extract_links

    def scrap(self, dom):
        main_list = self._extract_links(dom)

        return list(map(lambda item: {'name': item.get_text()}, main_list))
