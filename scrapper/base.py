# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging
from abc import ABC, abstractmethod

from scrapper.util import CsvExporter, DataCleaner

"""
Base scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class CsvScrapper(ABC):
    """
    Scraps a page, cleans up the data and stores it into a CSV file.

    This will only parse the DOM from a single page. Any additional operation, such as the actual scrapping, is delegated
    to the _transform method.
    """

    def __init__(self, url, output_file, headers):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = url
        self.exporter = CsvExporter(output_file, headers)
        # Data sorted by the first header
        self.cleaner = DataCleaner(headers[0])

    def scrap(self):
        self.logger.info('Scrapping %s', self.url)

        # Parses the DOM from the HTML page
        html = requests.get(self.url)
        dom = BeautifulSoup(html.text, 'html.parser')

        # Transforms DOM into the output data
        self.logger.debug('Transforming DOM')
        data = self._transform(dom)

        # Cleans up data
        self.logger.debug('Final data clean up')
        self.cleaner.clean_up(data)

        # Exports data
        self.logger.debug('Exporting data')
        self.exporter.export(data)

        self.logger.info('Finished scrapping %s', self.url)

    @abstractmethod
    def _transform(self, dom):
        """
        Extracts the data from the DOM.

        Returns
        -------
        data
            list of data parsed from the DOM
        """
        pass


class BaseListScrapper(CsvScrapper):
    """
    Scrapper for list pages. Takes all the links from a list, goes to each of them and scraps the target page.
    """

    def __init__(self, root_url, list_page, output_file, headers, inner_page_scrapper):
        super(BaseListScrapper, self).__init__(root_url + list_page, output_file, headers)
        self.root_url = root_url
        self.inner_page_scrapper = inner_page_scrapper

    def _transform(self, dom):
        main_list = self._extract_links(dom)

        # Takes the relative path and appends it to the root URL
        sub_urls = list(map(lambda item: self.root_url + item['href'], main_list))

        self.logger.info('Found %d inner pages to scrap', len(sub_urls))
        self.logger.debug('Inner pages: %s', len(sub_urls))

        # Scraps inner pages
        data = []
        for index, sub_url in enumerate(sub_urls):
            if index % 10 == 0:
                self.logger.info('Scrapping URL %d of %d', index, len(sub_urls))
            self.logger.debug('Scrapping inner page: %s', sub_url)
            scrapped = self.inner_page_scrapper.scrap(sub_url)
            if isinstance(scrapped, list):
                data = data + scrapped
            else:
                data.append(scrapped)

        return data

    @abstractmethod
    def _extract_links(self, dom):
        """
        Extracts the links for the subpages from the DOM.

        Returns
        -------
        list
            a list of link elements
        """
        pass
