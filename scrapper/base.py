# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import logging
from abc import ABC, abstractmethod
import re

"""
Base scrappers
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'


class CsvExport:

    def __init__(self, output_file, headers):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_file = output_file
        self.headers = headers

    def export(self, data):
        with open(self.output_file, mode='w', newline='') as data_file:
            fieldnames = self.headers
            output_writer = csv.DictWriter(data_file, fieldnames=fieldnames)

            output_writer.writeheader()
            output_writer.writerows(data)

        self.logger.info('Saved {} rows to {}'.format(len(data), self.output_file))


class DataCleaner:

    def __init__(self, key):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.key = key

    def clean_up(self, data):
        # Sorts data by name
        data = sorted(data, key=lambda d: d[self.key])

        # Removes data in parenthesis from name
        for item in data:
            item[self.key] = re.sub(" \(.*\)", "", item[self.key])


class BaseScrapper(ABC):
    """
    Generic scrapper.
    """

    def __init__(self, url, output_file, headers):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = url
        self.exporter = CsvExport(output_file, headers)
        self.cleaner = DataCleaner(headers[0])

    def scrap(self):
        list_url = self.url

        self.logger.info('Scrapping {}'.format(list_url))

        html = requests.get(list_url)
        dom = BeautifulSoup(html.text, 'html.parser')

        data = self.scrap_data(dom)

        # Cleans up data
        self.cleaner.clean_up(data)

        # Exports data
        self.exporter.export(data)

        self.logger.info('Finished scrapping {}'.format(list_url))

    @abstractmethod
    def scrap_data(self, dom):
        """
        Extracts the data from the DOM.

        Returns
        -------
        data
            list of data parsed from the DOM
        """
        pass


class BaseListScrapper(BaseScrapper):
    """
    Scrapper for list pages. Will find all the subpages and scrap each of them.
    """

    def __init__(self, root_url, list_page, output_file, headers):
        super(BaseListScrapper, self).__init__(root_url + list_page, output_file, headers)
        self.root_url = root_url

    def scrap_data(self, dom):
        main_list = self.extract_list_links(dom)

        sub_urls = list(map(lambda item: self.root_url + item['href'], main_list))

        self.logger.info('Found {} inner pages to scrap'.format(len(sub_urls)))

        # Scraps inner pages
        data = []
        for index, sub_url in enumerate(sub_urls):
            if index % 10 == 0:
                self.logger.info('Scrapping URL {} of {}'.format(index, len(sub_urls)))
            scrapped = self.scrap_inner_page(sub_url)
            if isinstance(data, list):
                data = data + scrapped
            else:
                data.append(scrapped)

        return data

    @abstractmethod
    def scrap_inner_page(self, sub_url):
        """
        Parses an inner page.

        Returns
        -------
        data
            list of data parsed from the page
        """
        pass

    @abstractmethod
    def extract_list_links(self, dom):
        """
        Extracts the links for the subpages from the DOM.

        Returns
        -------
        list
            a list of link elements
        """
        pass


class BaseListDescriptionScrapper(BaseListScrapper):
    """
    Scrapper for list pages. Will find all the subpages and scrap each of them.

    This is ready for pages based on a name and description set.
    """

    def __init__(self, root_url, list_page, output_file):
        super(BaseListDescriptionScrapper, self).__init__(root_url, list_page, output_file, ['name', 'url', 'description'])

    def scrap_inner_page(self, sub_url):
        html = requests.get(sub_url)
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

        return {'name': name, 'url': sub_url, 'description': description}

    @abstractmethod
    def extract_list_links(self, dom):
        """
        Extracts the links for the subpages from the DOM.

        Returns
        -------
        list
            a list of link elements
        """
        pass


class BaseNameListScrapper(BaseScrapper):
    """
    Scrapper for name list pages. Will find all the names in a page and store them in a list.
    """

    def __init__(self, root_url, list_page, output_file):
        super(BaseNameListScrapper, self).__init__(root_url + list_page, output_file, ['name'])

    def scrap_data(self, dom):
        main_list = self.extract_list(dom)

        return list(map(lambda item: {'name': item.get_text()}, main_list))

    @abstractmethod
    def extract_list(self, dom):
        """
        Extracts the list of names from the DOM.

        Returns
        -------
        list
            a list of text elements
        """
        pass
