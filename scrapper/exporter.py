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
        self._logger = logging.getLogger(self.__class__.__name__)
        self._output_file = output_file
        self._headers = headers

    def export(self, data):
        # Opens the output file and stores data
        with open(self._output_file, mode='w', newline='') as data_file:
            output_writer = csv.DictWriter(data_file, fieldnames=self._headers)

            output_writer.writeheader()
            output_writer.writerows(data)

        self._logger.info('Saved %d rows to %s', len(data), self._output_file)
