# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

from scrapper.exporter import CsvExporter
from scrapper.cleaner import DataCleaner

"""
Base scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class CsvScrapper(object):
    """
    Scraps a page, cleans up the data and stores it into a CSV file.

    This will only parse the DOM from a single page. Any additional operation, such as the actual scrapping, is delegated
    to the _transform method.
    """

    def __init__(self, url, output_file, headers):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._url = url
        self._exporter = CsvExporter(output_file, headers)
        # Data sorted by the first header
        self._cleaner = DataCleaner(headers[0])
        self._inner_parser = None

    @property
    def inner_parser(self):
        return self._inner_parser

    @inner_parser.setter
    def inner_parser(self, parser):
        self._inner_parser = parser

    def scrap(self):
        self._logger.info('Begins scrapping %s', self._url)

        # Parses the DOM from the HTML page
        html = requests.get(self._url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Transforms DOM into the output data
        self._logger.debug('Transforming DOM')
        data = self.inner_parser.scrap(dom)

        # Cleans up data
        self._logger.debug('Final data clean up')
        data = self._cleaner.clean_up(data)

        # Exports data
        self._logger.debug('Exporting data')
        self._exporter.export(data)

        self._logger.info('Finished scrapping %s', self._url)


class ListScrapper(object):
    """
    Scrapper for list pages. Takes all the links from a list, goes to each of them and scraps the target page.
    """

    def __init__(self, url, inner_page_scrapper, link_scrapper):
        super(ListScrapper, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._url = url
        self._inner_page_scrapper = inner_page_scrapper
        self._link_scrapper = link_scrapper

    def scrap(self, dom):
        self._logger.info('Scrapping links list')

        main_list = self._link_scrapper(dom)

        # Takes the relative path and appends it to the root URL
        sub_urls = list(map(lambda item: self._url + item['href'], main_list))

        # Scraps inner pages
        data = []
        total = len(sub_urls)
        self._logger.info('Found %d links to scrap', total)
        for index, sub_url in enumerate(sub_urls):
            self._logger.debug('Scrapping link (%d/%d): %s', index + 1, total, sub_url)
            scrapped = self._inner_page_scrapper.scrap(sub_url)
            if isinstance(scrapped, list):
                data = data + scrapped
            else:
                data.append(scrapped)

        return data
