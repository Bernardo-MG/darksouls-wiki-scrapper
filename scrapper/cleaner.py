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
        self._logger = logging.getLogger(self.__class__.__name__)
        self._key = key

    def clean_up(self, data):
        # Sorts data by defined key
        self._logger.debug('Sorting by column %s', self._key)
        cleaned = sorted(data, key=lambda d: d[self._key])

        # Cleans up data
        for item in cleaned:
            for key in item:
                value = item[key]
                if isinstance(value, str):
                    value = value.strip()
                item[key] = value

        return cleaned
