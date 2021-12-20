# -*- coding: utf-8 -*-

import csv
import logging

"""
Exporters to take the data out of the application.
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
