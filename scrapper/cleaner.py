# -*- coding: utf-8 -*-

import logging

"""
Cleaners to tidy up the data.
"""


class DataCleaner:
    """
    Cleans up the parsed data. As it may contain several formatting errors, this class will make sure it is
    readable. Very useful before saving it.
    """

    def __init__(self, key):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.key = key

    def clean_up(self, data):
        # Sorts data by defined key
        self.logger.debug('Sorting by column %s', self.key)
        data = sorted(data, key=lambda d: d[self.key])

        # Cleans up data
        for item in data:
            for key in item:
                value = item[key]
                value = value.strip()
                item[key] = value
