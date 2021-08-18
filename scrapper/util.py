# -*- coding: utf-8 -*-

import csv
import re
import logging

"""
Classes to help when scrapping.
"""


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

        self.logger.info('Saved %d rows to %s', len(data), self.output_file)


class DataCleaner:

    def __init__(self, key):
        self.key = key

    def clean_up(self, data):
        # Sorts data by defined key
        data = sorted(data, key=lambda d: d[self.key])

        # Removes data in parenthesis from name
        for item in data:
            value = item[self.key]
            value = re.sub(" \(.*\)", "", value)
            value = value.strip()
            item[self.key] = value
