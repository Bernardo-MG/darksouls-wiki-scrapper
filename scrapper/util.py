# -*- coding: utf-8 -*-

import csv
import logging

"""
Classes to help when scrapping.
"""


class CsvExporter:
    """
    Stores data into a CSV file. This file will be created, destroying any previous file.
    """

    def __init__(self, output_file, headers):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_file = output_file
        self.headers = headers

    def export(self, data):
        # Opens the output file and stores data
        with open(self.output_file, mode='w', newline='') as data_file:
            output_writer = csv.DictWriter(data_file, fieldnames=self.headers)

            output_writer.writeheader()
            output_writer.writerows(data)

        self.logger.info('Saved %d rows to %s', len(data), self.output_file)


class DataCleaner:
    """
    Cleans up the data before saving. As it may contain several formatting errors, this class will make sure it is
    readable.
    """

    def __init__(self, key):
        self.key = key

    def clean_up(self, data):
        # Sorts data by defined key
        data = sorted(data, key=lambda d: d[self.key])

        # Removes data in parenthesis from name
        for item in data:
            for key in item:
                value = item[key]
                value = value.strip()
                item[key] = value
