# -*- coding: utf-8 -*-

import logging
import configparser
import os

from scrapper.item.catalyst import CatalystScrapper
from scrapper.item.catalyst_attr_adjustment import CatalystAttributeAdjustmentScrapper
from scrapper.item.shield import ShieldScrapper
from scrapper.item.shield_levels import ShieldLevelsScrapper
from scrapper.item.talisman import TalismanScrapper
from scrapper.item.talisman_attr_adjustment import TalismanAttributeAdjustmentScrapper
from scrapper.item.weapon import WeaponScrapper

logging.basicConfig(
    filename='scrapper.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

# for handler in logging.root.handlers:
#     handler.addFilter(logging.Filter(['base', 'list', 'relation']))

config_path = 'config/urls.cfg'

url_config = configparser.ConfigParser()
url_config.read(config_path)

url_root = url_config['common']['root']

if not os.path.exists('output'):
    os.makedirs('output')

scrappers = []

# for scrapper in scrappers:
#     scrapper.scrap()

# parser = WeaponTypeScrapper(url_root)
# parser.scrap()

parser = TalismanAttributeAdjustmentScrapper()
parser.scrap()
parser = CatalystAttributeAdjustmentScrapper()
parser.scrap()
